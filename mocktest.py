from email import header
from lib2to3.pgen2 import token
from site import check_enableusersite
from urllib import response
import pytest
from app import db
from flask import Flask, session
import app
import base64
import json
from difflib import SequenceMatcher
import random
import string
from app import app


class Test_API:

    client = app.test_client()
    word = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    r1 = random.randint(0, 10)
    id1 = 1
    id2 = 2

    @pytest.fixture(autouse=True, scope='session')
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///practice.db'

#     # 1
    
#     def test_seller_success_login(self):
#         print("HI")
#         url = "/api/public/login"
#         user_credentials = 'apple:pass_word'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         print("credential [[[[[[[[[[[[")
#         print(user_credentials)
#         print(valid_credentials)
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 200
#         assert response.json['token']
#     '''
#     # 2
#     '''
#     def test_seller_fail_login(self):
#         url = "/api/public/login"
#         user_credentials = 'admin:nopassword'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 401
#         #assert response.json['token']
#     '''
#     # 3
#     '''
#     def test_consumer_success_login(self):
#         url = "/api/public/login"
#         user_credentials = 'jack:pass_word'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 200
#         assert response.json['token']
#     '''
#     # 4
#     '''
#     def test_consumer_fail_login(self):
#         url = "/api/public/login"
#         user_credentials = 'bob:nopassword'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 401
#         #assert response.json['token']
#     '''
#     # 5
#     '''
#     def test_public_endpoint_success(self):
#         word = 'crocin'
#         url = '/api/public/product/search?keyword='+word
#         headers = {'Content-Type': "application/json"}
#         response = self.client.get(url, headers=headers)
#         ans = response.get_data(as_text=True).strip()
#         check_ans = '[{"category":{"category_id":5,"category_name":"Medicines"},"price":10.0,"product_id":2,"product_name":"crocin","seller_id":4}]'
#         print(ans)
#         print(check_ans)
#         assert ans == check_ans
#         assert response.status_code == 200
#     '''
#     # 6
#     '''
#     def test_public_endpoint_failure(self):
#         word1 = 'noooo'
#         url = '/api/public/product/search?keyword='+word1
#         headers = {'Content-Type': "application/json"}
#         response = self.client.get(url, headers=headers)
#         ans = response.get_data(as_text=True).strip()
#         # check_ans='[{"category":{"category_id":5,"category_name":"Medicines"},"price":10.0,"product_id":2,"product_name":"crocin","seller_id":4}]'
#         # print(ans)
#         # print(check_ans)
#         #assert ans==check_ans
#         assert response.status_code == 400
#     '''
#     # 7 
#     '''
#     def test_seller_products_success(self):

#         url = "/api/public/login"
#         user_credentials = 'apple:pass_word'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 200
#         token = response.json['token']
#         print(token)
#         print("token aagya ", token)

#         url1 = '/api/auth/seller/product'
#         headers1 = {'Content-Type': "application/json",
#                     'x-access-token': ""+token}
#         response = self.client.get(url1, headers=headers1)
#         ans = response.get_data(as_text=True).strip()
#         print(ans)
#         check_ans = '[{"category":{"category_id":2,"category_name":"Electronics"},"price":80000.0,"product_id":4,"product_name":"phone","seller_id":3}]'
#         print(check_ans)
#         assert ans == check_ans
#         assert response.status_code == 200
#     '''
#     #8
#     '''
#     def test_seller_products_failure_consumer_login(self):

#         url = "/api/public/login"
#         user_credentials = 'jack:pass_word'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 200
#         token = response.json['token']
#         url1 = '/api/auth/seller/product'
#         headers1 = {'Content-Type': "application/json",
#                     'x-access-token': ""+token}
#         response = self.client.get(url1, headers=headers1)
#         assert response.status_code == 403
#     '''

# #     #9
#     '''
#     def test_seller_products_failure_without_token(self):
#         url = "/api/public/login"
#         user_credentials = 'apple:pass_word'
#         valid_credentials = base64.b64encode(
#             user_credentials.encode('UTF-8')).decode('UTF-8')
#         response = self.client.get(
#             url, headers={'Authorization': 'Basic ' + valid_credentials})
#         assert response.status_code == 200
#         token = response.json['token']

#         url1 = '/api/auth/seller/product'
#         headers1 = {'Content-Type': "application/json"
#                     }
#         response1 = self.client.get(url1, headers=headers1)

#         assert response1.status_code == 401
#         s = SequenceMatcher(
#             lambda x: x == " ", response1.json['Message'].strip(), "Token is missing")
#         match = round(s.ratio(), 3)
#         assert match > 0.8
#     '''
    
#     #10
#     '''
#     def test_seller_products_failure_invalid_token(self):

#         url="/api/public/login"
#         user_credentials='apple:pass_word'
#         valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
#         response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
#         assert response.status_code==200
#         token='invalidtokeninput'
#         print(token)
#         print("token aagya ",token)

#         url1='/api/auth/seller/product'
#         headers1={'Content-Type':"application/json",'x-access-token':""+token}
#         response1=self.client.get(url1,headers=headers1)

#         assert response1.status_code == 401
#         s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is invalid")
#         match=round(s.ratio(),3)
#         assert match > 0.8
#     '''

    #11 
    # '''
    # def test_seller_single_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/1'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     response1=self.client.get(url1,headers=headers1)
    #     ans=response1.get_data(as_text=True).strip()
    #     check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":8768678.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
    #     print(ans)
    #     print(check_ans)
    #     assert ans==check_ans
    #     assert response.status_code== 200
    

    # # 12
    # def test_seller_single_product_failure_different_seller(self):

    #     url="/api/public/login"
    #     user_credentials='glaxo:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/1'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     response1=self.client.get(url1,headers=headers1)
    #     # ans=response1.get_data(as_text=True).strip()
    #     # check_ans='[{"category":{"category_id":2,"category_name":"Electronics"},"price":29190.0,"product_id":1,"product_name":"ipad","seller_id":3}]'
    #     # print(check_ans)
    #     # assert ans==check_ans
    #     assert response1.status_code== 404


    # # # 13
    # def test_seller_single_product_failure_consumer_login(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/1'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     response1=self.client.get(url1,headers=headers1)
        
    #     assert response1.status_code== 403

    # # #14
    # def test_seller_single_product_failure_invalid_token(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token='invalidtoken'
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/1'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     response1=self.client.get(url1,headers=headers1)
    #     assert response1.status_code== 401
        
    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is invalid")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
     

    # # #15
    # def test_seller_single_product_failure_without_token(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/1'
    #     headers1={'Content-Type':"application/json"}
    #     response1=self.client.get(url1,headers=headers1)
    #     assert response1.status_code== 401
       
    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is missing")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
 
#     #16
    # def test_seller_add_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
     

    #     url1='/api/auth/seller/product'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":18,"product_name":"phone","price":80000,"category_id":2}'
    #     response1=self.client.post(url1,headers=headers1,data=payload1)
    #     ans=response1.get_data(as_text=True).strip()

    #     assert ans=='18'
    #     assert response1.status_code==201
    # '''

#     #17 prod id badal k chekc krna
    
    # def test_seller_add_product_failure_consumer(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3,"product_name":"phone","price":80000,"category_id":2}'
    #     response1=self.client.post(url1,headers=headers1,data=payload1)
    #     assert response1.status_code==403
    

#     #18
    
    # def test_seller_add_product_failure_sameproductagain(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3,"product_name":"phone","price":80000,"category_id":2}'
    #     response1=self.client.post(url1,headers=headers1,data=payload1)
    #     assert response1.status_code==409
    


#     #19
    # def test_seller_update_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3,"price":8768678}'
    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     assert response1.status_code==200
    

#     '''
#     #20
    # def test_seller_update_product_failure_another_seller(self):

    #     url="/api/public/login"
    #     user_credentials='glaxo:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
       

    #     url1='/api/auth/seller/product'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3,"price":8768678}'
    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     assert response1.status_code==404
    # '''

#     '''
#     #21
    # def test_seller_update_product_failure_consumer(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3,"price":8768678}'
    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     assert response1.status_code==403
    


    # 22
    # def test_seller_delete_product_failure_anotherseller(self):

    #     url="/api/public/login"
    #     user_credentials='glaxo:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/3'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3,"price":8768678}'
    #     response1=self.client.delete(url1,headers=headers1)
    #     assert response1.status_code == 404
    # '''

#     # 23'''
    # def test_seller_delete_product_failure_consumer(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/3'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}

    #     response1=self.client.delete(url1,headers=headers1)
    #     assert response1.status_code==403
    # '''


#     # 24 data hi nhi hai kya batayee'''
    # def test_seller_delete_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/seller/product/3'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}

    #     response1=self.client.delete(url1,headers=headers1)
    #     assert response1.status_code == 200
    

#     '''25
    # def test_consumer_cart_success(self):
    #     url='/api/public/login'
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     response1=self.client.get(url1,headers=headers1)
    #     ans=response1.get_data(as_text=True).strip()
    #     print("in test")
    #     print(ans)

    #     #check_ans='[{"cart_id":"1","cartproducts":{"cp_id":1,"product":{"category":{"category_id":5,"category_name":"Medicines"},"price":10.0,"product_id":2,"product_name":"crocin"}},"total_amount":20.0}]'
    #     check_ans='[{"cart_id":"3","cartproducts":{"cp_id":4,"product":{"category":{"category_id":2,"category_name":"Electronics"},"price":80000.0,"product_id":4,"product_name":"phone"}},"total_amount":2222.0}]'
        
    #     print("in test")
    #     print(check_ans)
    #     assert ans==check_ans
    #     assert response.status_code== 200
    


#     #26
    # def test_consumer_cart_failure_without_token(self):
    #     url='/api/public/login'
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json"}
    #     response1=self.client.get(url1,headers=headers1)
    #     assert response1.status_code== 401

    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is missing")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8


#     #27
    # def test_consumer_cart_failure_invalid_token(self):
    #     url='/api/public/login'
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token='invalidtokeninput'

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     response1=self.client.get(url1,headers=headers1)
    #     assert response1.status_code== 401

    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is invalid")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
    #

#     #28
    # def test_consumer_add_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
     

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":1,"quantity":1}'
    #     response1=self.client.post(url1,headers=headers1,data=payload1)
    #     ans=response1.get_data(as_text=True).strip()

    #     assert ans=='29210.0'
    #     assert response1.status_code==200

    #29 working
    # def test_consumer_add_product_failure_sameproduct(self):

    #         url="/api/public/login"
    #         user_credentials='jack:pass_word'
    #         valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #         response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #         assert response.status_code==200
    #         token=response.json['token']
        

    #         url1='/api/auth/consumer/cart'
    #         headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #         payload1='{"product_id":2,"quantity":2}'
    #         response1=self.client.post(url1,headers=headers1,data=payload1)
            
    #         assert response1.status_code==409



#    30 working
    # def test_consumer_add_product_failure_seller_login(self):

    #         url="/api/public/login"
    #         user_credentials='apple:pass_word'
    #         valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #         response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #         assert response.status_code==200
    #         token=response.json['token']
        

    #         url1='/api/auth/consumer/cart'
    #         headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #         payload1='{"product_id":2,"quantity":2}'
    #         response1=self.client.post(url1,headers=headers1,data=payload1)
            
    #         assert response1.status_code==403

       
    

#   31  working
    # def test_consumer_add_product_failure_token_invalid(self):
        
    #     url='/api/public/login'
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token='invalidtokeninput'

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
        
    #     payload1='{"product_id":2,"quantity":2}'
    #     response1=self.client.get(url1,headers=headers1,data=payload1)
    #     assert response1.status_code== 401

    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is invalid")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
    

#     #32
    # def test_consumer_add_product_failure_token_missing(self):

    #     url='/api/public/login'
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json"}
    #     payload1='{"product_id":2,"quantity":2}'
        
    #     response1=self.client.get(url1,headers=headers1,data=payload1)
    #     assert response1.status_code== 401

    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is missing")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8


#    33 working
    # def test_consumer_update_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
       

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":1,"quantity":2}'

    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     ans=response1.get_data(as_text=True).strip()
    #     assert ans=='17537356.0'
    #     assert response1.status_code==200
    

#    34
    # def test_consumer_update_product_failure_seller_login(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":1,"quantity":2}'

    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     ans=response1.get_data(as_text=True).strip()

    #     assert response1.status_code==403
    

#     '''35
    # def test_consumer_update_product_failure_invalid_token(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token='invalid'
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":1,"quantity":2}'

    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     ans=response1.get_data(as_text=True).strip()

    #     assert response1.status_code==401
    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is invalid")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
    

#     '''36
    # def test_consumer_update_product_failure_missing_token(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token='invalid'
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json"}
    #     payload1='{"product_id":1,"quantity":2}'

    #     response1=self.client.put(url1,headers=headers1,data=payload1)
    #     ans=response1.get_data(as_text=True).strip()

    #     assert response1.status_code==401
    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is missing")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
    

#     '''37
    # def test_consumer_delete_product_failure_seller_login(self):

    #     url="/api/public/login"
    #     user_credentials='apple:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":1}'

    #     response1=self.client.delete(url1,headers=headers1,data=payload1)

    #     assert response1.status_code==403
    

#   #38
    # def test_consumer_delete_product_failure_invalid_token(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token='invalid'
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":1}'

    #     response1=self.client.delete(url1,headers=headers1,data=payload1)

    #     assert response1.status_code==401
    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is invalid")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
    



#     '''39
    # def test_consumer_delete_product_failure_missing_token(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json"}
    #     payload1='{"product_id":17}'

    #     response1=self.client.delete(url1,headers=headers1,data=payload1)

    #     assert response1.status_code==401
    #     s=SequenceMatcher(lambda x:x == " ", response1.json['Message'].strip(),"Token is missing")
    #     match=round(s.ratio(),3)
    #     assert match > 0.8
    
    
#     '''40
    # def test_consumer_delete_product_success(self):

    #     url="/api/public/login"
    #     user_credentials='jack:pass_word'
    #     valid_credentials=base64.b64encode(user_credentials.encode('UTF-8')).decode('UTF-8')
    #     response=self.client.get(url,headers={'Authorization':'Basic '+ valid_credentials})
    #     assert response.status_code==200
    #     token=response.json['token']
    #     print(token)
    #     print("token aagya ",token)

    #     url1='/api/auth/consumer/cart'
    #     headers1={'Content-Type':"application/json",'x-access-token':""+token}
    #     payload1='{"product_id":3}'

    #     response1=self.client.delete(url1,headers=headers1,data=payload1)

    #     ans=response1.get_data(as_text=True).strip()
    #     assert ans=='17537356.0'
    #     assert response1.status_code==200
    

 