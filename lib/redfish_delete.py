import os
import shutil

def delete_folder(path):
	if os.path.isdir(path):	
		try:
			shutil.rmtree(path)
		except Exception as e:
			print(e)
			return False
		return True
	else:
		print("No find the folder")
		return False
