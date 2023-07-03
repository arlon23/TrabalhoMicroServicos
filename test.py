import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import *


class FileUploadTest(unittest.TestCase):
    
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        # self.imageId = -1
    
    def test_1_file_upload_1(self):
        # Open a file for testing
        with open('test_file.txt', 'rb') as file:
            # Send a POST request to the file upload endpoint
            response = self.app.post('/files-api', data={'files': file, 'post_id': 10}, headers={'auth-token': 'user-2'})

            self.__class__.imageId = response.data

            # Assert the response status code and content
            self.assertEqual(response.status_code, 201)

    def test_1_file_upload_extension_invalid(self):
        # Open a file for testing
        with open('test_file.doc', 'rb') as file:
            # Send a POST request to the file upload endpoint
            response = self.app.post('/files-api', data={'files': file, 'post_id': 10}, headers={'auth-token': 'user-2'})

            # self.__class__.imageId = response.data

            # Assert the response status code and content
            self.assertEqual(response.status_code, 400)

    def test_1_file_upload_bad_words(self):
        # Open a file for testing
        with open('test_file_bad_words.txt', 'rb') as file:
            # Send a POST request to the file upload endpoint
            response = self.app.post('/files-api', data={'files': file, 'post_id': 10}, headers={'auth-token': 'user-2'})

            # self.__class__.imageId = response.data

            # Assert the response status code and content
            self.assertEqual(response.status_code, 400)

    def test_1_file_upload_forbidden(self):
        # Open a file for testing
        with open('test_file.txt', 'rb') as file:
            # Send a POST request to the file upload endpoint
            response = self.app.post('/files-api', data={'files': file, 'post_id': 10}, headers={'auth-token': ''})

            # self.__class__.imageId = response.data

            # Assert the response status code and content
            self.assertEqual(response.status_code, 403)

    def tearDown(self):
        # Clean up any resources if needed
        pass

    def test_list_post_success(self):
        post_id = 1

        # Send a GET request to the '/list' route with the post_id
        response = self.app.get(f'/files-api/{post_id}', headers={'auth-token': 'user-2'})

        # Print the response (for debugging purposes)
        # print(response)

        # Verify if the response has the expected status code
        assert response.status_code == 200

    def test_list_post_forbidden(self):
        post_id = 1

        # Send a GET request to the '/list' route with the post_id
        response = self.app.get(f'/files-api/{post_id}', headers={'auth-token': ''})

        # Print the response (for debugging purposes)
        # print(response)

        # Verify if the response has the expected status code
        assert response.status_code == 403

    # def test_2_list_post_failure(self):
    #     post_id = 2

    #     # Send a GET request to the '/list' route with the post_id
    #     response = self.app.get(f'/list/{post_id}')

    #     # Print the response (for debugging purposes)
    #     print('list')
    #     print(response)

    #     # Verify if the response has the expected status code
    #     assert response.status_code == 404


    def test_3_list_all(self):
        # Send a GET request to the '/list' route
        response = self.app.get('/files-api')

        # Print the response (for debugging purposes)
        # print(response)

        # Verify if the response has the expected status code
        assert response.status_code == 200


    def test_9_delete_success(self):
        for uploadedImages in json.loads(self.__class__.imageId.decode())['data']:
            uploadedImageId = uploadedImages['image_id']
        # Send a DELETE request to the '/delete' route with the file_id
        response = self.app.delete(f'/files-api/{uploadedImageId}', headers={'auth-token': 'user-2'})

        # Verify if the response has the expected status code
        assert response.status_code == 200
    
    def test_8_delete_forbidden(self):
        for uploadedImages in json.loads(self.__class__.imageId.decode())['data']:
            uploadedImageId = uploadedImages['image_id']
        # Send a DELETE request to the '/delete' route with the file_id
        response = self.app.delete(f'/files-api/{uploadedImageId}', headers={'auth-token': ''})

        # Verify if the response has the expected status code
        assert response.status_code == 403


    def test_delete_failure(self):
        file_id = -1

        # Send a DELETE request to the '/delete' route with the file_id
        response = self.app.delete(f'/files-api/{file_id}', headers={'auth-token': 'user-2'})

        # Print the response (for debugging purposes)
        # print(response)

        # Verify if the response has the expected status code
        assert response.status_code == 404
