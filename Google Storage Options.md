Task 1: Deploy a web server VM instance

Navigate to Compute Engine > VM instances in the Google Cloud Console.
Click "Create Instance" and name it as "bloghost".
Select the appropriate region, machine type, and boot disk (Debian GNU/Linux 11).
Allow HTTP traffic and expand the "Management" section.
Enter the provided startup script for installing Apache, PHP, and MySQL.
Click "Create" and wait for the instance to launch.
Copy the internal and external IP addresses of the newly created instance.
Task 2: Create a Cloud Storage bucket using the gcloud storage command line

Open Cloud Shell from the top right toolbar in the Google Cloud Console.
Set the location environment variable based on the provided commands.
Create a Cloud Storage bucket using the project ID as the bucket name.
Retrieve a banner image from a publicly accessible Cloud Storage location.
Copy the banner image to the newly created Cloud Storage bucket.
Modify the Access Control List of the uploaded image to make it readable by everyone.
Task 3: Create the Cloud SQL instance

Navigate to SQL in the Google Cloud Console.
Click "Create instance" and select MySQL as the database engine.
Name the instance as "blog-db" and set a root password.
Choose the appropriate Cloud SQL edition and single zone deployment.
Set the region and zone matching the bloghost instance.
Click "Create Instance" and wait for the deployment to finish.
Copy the Public IP address of the SQL instance for later use.
Add a user account (blogdbuser) with a password.
Configure the network connection by adding the external IP address of the bloghost instance.
Task 4: Configure an application in a Compute Engine instance to use Cloud SQL

SSH into the bloghost VM instance from the VM instances list.
Change the working directory to the document root of the web server.
Use a text editor to edit the index.php file.
Paste the provided PHP code into the file and save it.
Restart the Apache web server.
Open a web browser and navigate to the bloghost's external IP address.
Note the database connection failure message.
SSH back into the bloghost instance and edit the index.php file again.
Replace placeholders with actual Cloud SQL instance details.
Restart the Apache web server and reload the web page to confirm the successful database connection.
Task 5: Configure an application in a Compute Engine instance to use a Cloud Storage object

Navigate to Cloud Storage > Buckets in the Google Cloud Console.
Open the bucket named after your GCP project.
Copy the URL of the banner image from the bucket.
SSH into the bloghost VM instance.
Change the working directory to the document root of the web server.
Use a text editor to edit the index.php file.
Insert the HTML markup for the banner image URL above the existing content.
Save the file, restart the Apache web server, and reload the web page.
Verify that the banner image is now displayed on the web page.
Conclusion:

Reflect on the tasks completed in the lab and their importance in understanding Google Cloud fundamentals.
Consider any challenges faced during the lab and how they were resolved.
Share any insights gained from completing the lab exercises.
Rate the lab experience based on satisfaction and provide feedback if necessary.
Click "End Lab" to terminate the lab session and clean up resources.