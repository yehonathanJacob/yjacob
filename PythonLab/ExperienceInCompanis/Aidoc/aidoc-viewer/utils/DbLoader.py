import os
import re
import json
import logging
from shutil import copyfile
from datetime import datetime

from scan import Scan
from models import models
from utils.db import db, get_one_or_create
from utils.PasswordGenerator import PasswordGenerator

from dicomaizer.common.uid import string2hash


class DbLoader(object):
    def init(self, worklist_dir, findings_dir, ct_scans_dir, scan_compressor, logger=None):
        self.worklist_dir = worklist_dir
        self.findings_dir = findings_dir
        self.ct_scans_dir = ct_scans_dir
        self.scan_compressor = scan_compressor
        self.logger = logger or logging

    def load_work_item_findings(self, work_item, body_part, series, filename):
        with open(filename) as data_file:
            data = json.load(data_file)

            massive_bleeding = data.get('massive_bleed', False)
            series.massive_bleeding = massive_bleeding

            for key, value in data['finding_dict'].items():
                order = int(key)
                key_slice = value['key_slice']
                visualization_type = value['visualization_type']
                input_source_index = value.get('input_source_index', 0)
                comment = value.get('comment', '')
                status = value.get('status', 'pristine')
                locations = json.dumps(value['slice_dict'])
                label = value.get('label', 'Finding')
                finding_uid = None
                contour = json.dumps(value['contour']) if 'contour' in value.keys() and value['contour'] is not None else None
                if 'finding_uid' in value:
                    finding_uid = value['finding_uid']

                finding = models.Finding(series.work_item_id, series.id, finding_uid, status, label, key_slice,
                                         visualization_type, locations, order, original_locations=locations,
                                         comment=comment, input_source_index=input_source_index, contour=contour)
                db.session.add(finding)

        db.session.commit()

    def load_scan(self, work_item, body_part, scan, overwrite_volumes=False, findings_should_be_loaded_from_files=False):
        create_method_kwargs = {
            'plane': scan.plane
        }

        series, work_item_just_created = get_one_or_create(models.Series, create_method_kwargs=create_method_kwargs,
                                            work_item_id=work_item.id, uid=scan.uid.strip())

        if findings_should_be_loaded_from_files:
                findings_filename = self.get_findings_file(scan.uid)
                if os.path.isfile(findings_filename) and os.path.getsize(findings_filename) > 0:
                    self.load_work_item_findings(work_item, body_part, series, findings_filename)

        # Compress scan pixel data to improve load performance
        self.scan_compressor.compress(scan.uid, overwrite_volumes)

        return series, work_item_just_created

    def get_findings_file(self, series_uid):
        findings_filename = os.path.join(self.findings_dir, series_uid + '.json')

        if os.path.isfile(findings_filename):
            return findings_filename

        # for backwards compatibility check if there is a file with findings_ prefix,
        # should be removed in the near future
        return os.path.join(self.findings_dir, 'findings_' + series_uid + '.json')

    def load_study(self, study_uid, scans, user_id, worklist_metadata, overwrite_volumes=False,
                   load_finding_files=True, overwrite_findings_metadata=False):
        accession_number = scans[0].metadata.get('AccessionNumber', study_uid)
        patient_name = scans[0].name
        body_part = scans[0].body_part
        scan_planes = {scan.uid: scan.plane for scan in scans}

        self.validate_study(scan_planes, scans, study_uid)
        # Add the study to the DB
        create_method_kwargs = {
            'patient_name': patient_name,
            'patient_id': scans[0].patient_id,
            'study_date': scans[0].date,
            'study_time': scans[0].time,
            'accession_number': accession_number,
            'body_part': body_part,
            'analyzed_by_aidoc': worklist_metadata[
                'analyzed_by_aidoc'] if 'analyzed_by_aidoc' in worklist_metadata else True
        }

        work_item, work_item_just_created = get_one_or_create(models.WorkItem,
                                               create_method_kwargs=create_method_kwargs,
                                               user_id=user_id, uid=study_uid.strip())

        has_massive_bleeding = False

        num_of_series_created = 0
        findings_should_be_loaded_from_files = load_finding_files and work_item.analyzed_by_aidoc and \
                                               (overwrite_findings_metadata or work_item_just_created)
        if findings_should_be_loaded_from_files:
            self.delete_work_item_findings(work_item)

        for scan in scans:
            series, series_created = self.load_scan(work_item, body_part, scan,
                                                    overwrite_volumes, findings_should_be_loaded_from_files)
            if series_created:
                num_of_series_created += 1
            if series.massive_bleeding:
                has_massive_bleeding = True

        work_item.massive_bleeding = has_massive_bleeding
        db.session.commit()

        return work_item_just_created, num_of_series_created

    def validate_study(self, scan_planes, scans, study_uid):
        if len(scans) not in (1, 3):
            raise Exception('Unexpected number of series found for study_uid {}, only 1 or 3 series per study '
                            'are supported. You loaded the following series: {}'.format(study_uid, str(scan_planes)))

    def load_worklist(self, user, worklist_filename, delete_user_metadata_before_loading=False,
                      overwrite_findings_metadata=False, overwrite_volumes=False):
        if delete_user_metadata_before_loading:
            for work_item in user.worklist:
                self.delete_work_item(work_item)

        worklist_report = []
        try:
            uids, worklist_metadata = self.load_worklist_data(worklist_filename)
        except IllegalWorklistFormat as e:
            self.logger.error(e)
            uids = []
            worklist_metadata = None
            worklist_report.append('{}'.format(e))


        # Collect study information
        studies = {}
        for uid in uids:
            try:
                try:
                    scan = Scan.fromID(uid, self.ct_scans_dir, read_volume=False)
                except IOError:
                    self.logger.warning('Cannot find CTscan file for uid {}'.format(uid))
                    worklist_report.append({uid: 'No scan file {} found'.format(string2hash(uid))})
                    continue
                if 'StudyInstanceUID' in scan.metadata:
                    study_uid = scan.metadata['StudyInstanceUID']
                else:
                    self.logger.warning('Missing StudyInstanceUID for scan with uid %s - using accession number or '
                                        'series uid instead', uid)
                    if 'AccessionNumber' in scan.metadata:
                        study_uid = scan.metadata['AccessionNumber']
                    else:
                        study_uid = scan.uid

                curr_scan_should_have_findings = self._scan_should_have_findings(
                    scan, worklist_metadata[study_uid] if study_uid in worklist_metadata else {})
                load_finding_files = user.load_finding_files
                if load_finding_files and curr_scan_should_have_findings:
                    findings_filename = self.get_findings_file(scan.uid)
                    if not os.path.isfile(findings_filename):
                        self.logger.warning('Cannot locate findings JSON file for scan with uid "%s" - skipping',
                                            uid)
                        worklist_report.append({uid: 'No findings file'})
                        continue

                if study_uid not in studies:
                    studies[study_uid] = []

                # check for duplicate series uids in the worklist
                duplicate_found = False
                for added_scan in studies[study_uid]:
                    if added_scan.uid == scan.uid:
                        duplicate_found = True
                        break

                if duplicate_found:
                    self.logger.warning('Duplicate uid {} in worklist'.format(uid))
                    worklist_report.append({uid: 'Duplicate uid in worklist'})
                    continue

                studies[study_uid].append(scan)
            except Exception as e:
                self.logger.warning('Unknown error for uid {} string2hash {}'.format(uid, string2hash(uid)))
                worklist_report.append({uid: 'Unknown error for uid {} string2hash {}'.format(uid, string2hash(uid))})

        study_count = 0
        study_load_count = 0
        series_count = 0
        series_load_count = 0
        studies_report = []
        for study_uid, scans in studies.items():
            try:
                loaded, loaded_series = self.load_study(study_uid, scans, user.id, worklist_metadata[
                    study_uid] if study_uid in worklist_metadata else {}, overwrite_volumes, load_finding_files,
                                                        overwrite_findings_metadata)
                study_count += 1
                series_count += len(scans)

                if loaded:
                    study_load_count += 1

                series_load_count += loaded_series

            except Exception as e:
                self.logger.warning(str(e))
                studies_report.append({'study': study_uid, 'error': str(e)})

        return {'worklist_report': {'loaded': series_load_count, 'already-exist': series_count - series_load_count,
                                    'errors': worklist_report},
                'studies_report': {'loaded': study_load_count, 'already-exist': study_count - study_load_count,
                                   'errors': studies_report}}

    def load_worklist_data(self, worklist_filename):

        try:
            uids = []
            worklist_metadata = {}
            with open(worklist_filename) as f:
                worklist_json = json.load(f)
                for row in worklist_json:
                    series_list = row['series']

                    for uid in series_list:
                        uids.append(uid)
                        worklist_metadata[row["study_uid"]] = row
            return uids, worklist_metadata
        except Exception as e:
            self.logger.info('Failed to load file as json, loading as uids list' + str(e))
        with open(worklist_filename) as f:
            worklist_file_text = f.read()
            illegal_chars_regexp = '[,\'";\/]'
            contains_illegal_chars = bool(re.compile(r'{}'.format(illegal_chars_regexp)).search(worklist_file_text))
            if contains_illegal_chars:
                illegal_chars_string = ' '.join(illegal_chars_regexp[1:-1])
                error_msg = 'Worklist file contains illegal chararcters, at least one of the following: {}'.format(
                    illegal_chars_string)
                raise IllegalWorklistFormat(error_msg)
            else:
                uids = worklist_file_text.splitlines()
                uids = filter(None, uids)  # Remove empty lines

        return uids, {}



    def load_worklists(self, worklist_files, overwrite_series_metadata):
        report = {}
        for file in worklist_files:
            if file.filename == '':
                continue

            username = os.path.splitext(file.filename)[0]
            user = self.get_user(username)

            if user:
                worklist_file = os.path.join(self.worklist_dir, username)
                report[username] = self.load_worklist(user, worklist_file, overwrite_series_metadata)
            else:
                report[username] = 'User not found'

        return report

    def get_user(self, username):
        return db.session.query(models.User).filter_by(username=username).first()

    def load_user(self, username, name, worklist_file, delete_user_metadata_before_loading=False,
                  overwrite_volumes=False, overwrite_existing_findings_metadata=False):
        self.logger.info('Processing worklist for user {}'.format(username))

        if not os.path.isfile(worklist_file):
            self.logger.warning('Cannot find worklist for user ' + username + ' - skipping')
            return 'No worklist file ' + username + ' found'

        user, created = get_one_or_create(models.User,
                                          create_method_kwargs={'name': name, 'password': username[0] + '123456',
                                                                'created_on': datetime.now(), 'email': ''},
                                          username=username)
        if created:
            self.logger.info('Added new user {}'.format(user.username))

        return self.load_worklist(user, worklist_file,
                                  delete_user_metadata_before_loading=delete_user_metadata_before_loading,
                                  overwrite_findings_metadata=overwrite_existing_findings_metadata,
                                  overwrite_volumes=overwrite_volumes)

    def load_data(self):
        self.logger.info('Initializing DB data')
        users_file = os.path.join(self.worklist_dir, 'users')
        if not os.path.isfile(users_file):
            raise Exception('Cannot find user data file in directory ' + self.worklist_dir)

        load_report = []
        with open(users_file) as f:
            users = f.read().splitlines()

            for user_line in users:
                if not user_line:
                    continue

                parts = user_line.split('=')

                if len(parts) != 2:
                    self.logger.warning('Invalid user definition: ' + user_line)
                    continue

                username = parts[0]
                name = parts[1]
                user_report = self.load_user(username, name, os.path.join(self.worklist_dir, username))
                load_report.append({username: user_report})

        self.create_admin_user()

        self.logger.info('Initialized DB data')

        return load_report

    def create_admin_user(self):
        user = self.create_new_user(
            {'username': 'admin', 'name': 'Admin', 'role': 'admin', 'clone_from_user': 'demo', 'email': ''})
        self.logger.info('Admin user: {} '.format(user))

    def create_new_user(self, user_data):
        if 'role' in user_data:
            role = user_data['role']
        else:
            role = 'user'

        # check if user already exists
        user = self.get_user(user_data['username'])

        if user:
            return user.to_json_dict()

        # create new user
        password = PasswordGenerator.generate()
        print(password)

        load_finding_files = user_data.get('loadFindingFiles')

        user = models.User(username=user_data['username'], password=password, name=user_data['name'],
                           role=role, email=user_data['email'], created_on=datetime.now(),
                           load_finding_files=load_finding_files)

        db.session.add(user)
        db.session.commit()

        # clone the worklist file from the given user
        if 'clone_from_user' in user_data:
            clone_from = user_data['clone_from_user']

            worklist_file = os.path.join(self.worklist_dir, user_data['username'])

            copyfile(os.path.join(self.worklist_dir, clone_from), worklist_file)
            self.load_user(user.username, user.name, worklist_file)

        user_dict = user.to_json_dict()
        user_dict['password'] = password

        return user_dict

    def delete_user(self, user):

        worklist = user.worklist

        for work_item in worklist:
            self.delete_work_item(work_item)

        db.session.delete(user)
        db.session.commit()

    def delete_work_item(self, work_item):
        self.delete_work_item_findings(work_item)

        series = work_item.series
        for s in series:
            db.session.delete(s)

        db.session.delete(work_item)
        db.session.commit()

    def delete_work_item_findings(self, work_item):
        findings = work_item.findings
        for f in findings:
            db.session.delete(f)
        db.session.commit()


    def login_user(self, login_data):

        user = db.session.query(models.User).filter_by(username=login_data['username']).one()

        user.last_login_on = datetime.now()

        if 'browser_type' in login_data:
            user.last_login_from = login_data['browser_type']
        db.session.commit()

        return user

    @staticmethod
    def _scan_should_have_findings(scan, worklist_metadata):

        analyzed_by_aidoc = worklist_metadata[
            'analyzed_by_aidoc'] if 'analyzed_by_aidoc' in worklist_metadata else True

        if not analyzed_by_aidoc:
            return False
        return (scan.body_part == 'cspine' and scan.plane == 'sagittal') \
               or (scan.body_part == 'brain' and scan.plane == 'axial') \
               or (scan.body_part == 'thorax' and scan.plane == 'axial') \
               or (scan.body_part == 'abdomen' and scan.plane == 'axial')

class IllegalWorklistFormat(ValueError):
    pass

dbLoader = DbLoader()

