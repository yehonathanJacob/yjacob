from io import BytesIO
import os
import zipfile

from flask import Flask, Response

app = Flask(__name__)


@app.route('/download_tree_directoris', methods=['POST', 'GET'])
def download_tree_directoris():
	# Folder name in ZIP archive which contains the above files
	# E.g [thearchive.zip]/somefiles/file2.txt
	# FIXME: Set this to something better
	zip_subdir = "somefiles"
	zip_filename = "%s.zip" % zip_subdir

	# Open StringIO to grab in-memory ZIP contents
	s = BytesIO()
	foldername = "C:\\Users\\janjak2411\\GitProject"

	empty_dirs = []
	zip = zipfile.ZipFile(s, 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(foldername):
		# empty_dirs.extend([dir for dir in dirs if os.listdir(os.path.join(root, dir)) == []])
		# for name in files:
		#     zip.write(os.path.join(root, name))

		for dir in dirs:
			zif = zipfile.ZipInfo(os.path.join(root, dir) + "/")
			zip.writestr(zif, "")
		empty_dirs = []
	zip.close()

	# Grab ZIP file from in-memory, make response with correct MIME-type
	resp = Response(s.getvalue(), mimetype="application/x-zip-compressed", headers={
		"Content-Disposition":
			'attachment; filename=%s' % zip_filename
	})
	# ..and correct content-disposition

	return resp


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True, port=8080)
