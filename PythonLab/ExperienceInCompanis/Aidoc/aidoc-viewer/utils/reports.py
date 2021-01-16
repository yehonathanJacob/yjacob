import os
import logging

'''
Loads the doctors report from the file named by the accession number and returns its text
'''


class ReportsLoader:
    reports_dir: str = None

    def __init__(self, reports_dir: str):
        self.reports_dir = reports_dir

    def load_report(self, accession_number: str) -> str:
        report_file = os.path.join(self.reports_dir, accession_number + '.html')
        if os.path.exists(report_file):
            try:
                with open(report_file) as f:
                    return '\n'.join(f.readlines())
            except Exception as e:
                logging.exception('Failed to read the report file ' + report_file + '. ' + str(e), exc_info=True)

        return ''
