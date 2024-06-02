# Dash_App
## Deploying a DashApp to LAN to visualize Plotly graphs. 

### For Windows:
Ensure the APPNEW file is in the same directory as the CSV being used. Ensure pyinstaller is installed. Run the code below in the command prompt to package the app. This will create a spec file, a build folder, and a dist folder. To run the app, click on the app within the dist folder.

### CODE: pyinstaller --onefile --add-data "selected_rows.csv;." AppNew.py

### For macOS and Linux:
### CODE: pyinstaller --onefile --add-data "selected_rows.csv:." AppNew.py
