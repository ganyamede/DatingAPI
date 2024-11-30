# DatingAPI

The **Dating API** project is a backend for a dating platform built using **Flask**, **SQLAlchemy**, **JWT** and **Redis**. This project includes a RESTful API for user authentication, profile management, messages and likes, as well as integration with **Swagger UI** for easy testing and documentation.

## Features

- **JWT** for secure authentication and session management.
- **SQLAlchemy** for working with a database storing information about users, messages and likes.
- **Redis** for caching and improving performance.
- **Flask** is a lightweight framework for developing REST API.
- **Swagger UI** for interactive documentation and API testing.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ganyamede/DatingAPI.git
   cd DatingAPI
   ```

2. Create and activate the virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для macOS/Linux
   venv\Scriptsctivate  # Для Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application:

   ```bash
   python3 main.py
   ```

5. Open [Swagger UI](http://localhost/apidocs) to test the API.


6. Detailed description of the project, documentation
   
   ### You must use JWT ACCESS TOKEN everywhere 
   ### Except for the Authorization and Utility blocks in the documentation in the photo below

   # Utility
   ![telegram-cloud-photo-size-2-5357177841936100849-y](https://github.com/user-attachments/assets/8fa4ae21-516b-4898-82d5-97c9978d3576)

   - Get all cities in a country
   - Works with one country, expansion possible

   # Authorization
     ## Register
     ![telegram-cloud-photo-size-2-5357177841936100856-y](https://github.com/user-attachments/assets/cf716d3c-c07a-4635-bbd3-f8101769a347)
   
     - Profile registration
     - We do not return the JWT token here, we enter the data into the database and then wait for the login to localhost/api/sign
     - One-way password encryption, then we check
  
     ## Sign
     ![telegram-cloud-photo-size-2-5357177841936100859-y](https://github.com/user-attachments/assets/2772f20e-7858-4c85-84d7-65e3ea4c64f8)

     - After logging in, you return an access/refresh token, which it is advisable to immediately write to httpOnly

     ## Refresh to access
     ![telegram-cloud-photo-size-2-5357177841936100854-y](https://github.com/user-attachments/assets/f87bc240-e602-4940-a3c9-69adad4bcb42)

     - We receive information that is written in Refresh and write it to access
     - Suitable if the access service life has expired
  
  # Match
   ## MatchAll
   ![telegram-cloud-photo-size-2-5357552337314507948-y](https://github.com/user-attachments/assets/9c5f905c-4811-49b9-9b5f-64e79dc49be3)

   - List of all mutual sympathies

   ## Search
   ![telegram-cloud-photo-size-2-5357177841936100851-y](https://github.com/user-attachments/assets/ed6ffe8c-2af2-446f-8a84-82b61e532927)

   - We are looking for a partner for you based on the criteria
   - We receive your information and search for a pair for you, if it was found, we receive your cities, convert them to lat/long and calculate them in km, if the distance is less than 30 km, then we return

   ## Get like
   ![telegram-cloud-photo-size-2-5357177841936100850-y](https://github.com/user-attachments/assets/95e88648-9f97-4224-9e94-1ff9edca4511)

   - List of everyone who liked you

  # Likes
   ## Like
   ![telegram-cloud-photo-size-2-5357177841936100852-y](https://github.com/user-attachments/assets/bdf59b71-7b10-4fcd-b4ea-0242d130cfb2)
   
   - We write the like to the database, then display it in the list of likers for decision making
   - We also write the like to Redis so that it doesn't appear again within 24 hours

   ## Dislike
   ![telegram-cloud-photo-size-2-5357177841936100853-y](https://github.com/user-attachments/assets/c6bb8088-20f9-4f4f-8e86-917993076f87)

   - We skip the questionnaire, just like with the like, we write it to Redis so that it doesn't happen again
   - If you were liked, then we also delete the entry from the database

  # Client
   ## Select
   ![telegram-cloud-photo-size-2-5357177841936100860-y](https://github.com/user-attachments/assets/b3f83deb-3f48-42c3-ac07-dd22555251f7)

   - We receive full information about your profile, for display in the profile
   - Only about the profile, not email or passwords.
   - id/age/name/city/description/sex/search_sex/user_id (account ID, where is the email)

   ## Update
   ![telegram-cloud-photo-size-2-5357177841936100861-y](https://github.com/user-attachments/assets/8295c412-3f52-4861-8efc-30ecaf3620fc)

   - Creating a profile or updating information, the data is transmitted in the same way, checking whether there is an account occurs inside
   - Up to 6 photos, it is necessary to transmit age/name/city/description/sex/search_sex

  


   

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
