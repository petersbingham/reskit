cd ..

python alt_setup/create_setup_files.py
python alt_setup/update_readme.py

pip install -r reskit/utilities/requirements.txt --target=reskit/utilities

python alt_setup/clean.py
