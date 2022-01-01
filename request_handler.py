from http.server import BaseHTTPRequestHandler, HTTPServer
from animals import get_all_animals,get_single_animal,create_animal,delete_animal
from employees import get_all_employees,get_single_employee,create_employee,delete_employee
from locations import get_all_locations,get_single_location,create_location,delete_location
from customers import get_all_customers,get_single_customer,create_customer,delete_customer
import json

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self,path):
        path_params = path.split("/")
        resource = path_params[1]
        id=None
        
        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass
        return (resource,id)
        
    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        # Set the response code to 'Ok'
        self._set_headers(200)
        response = {}
        
        (resource, id) = self.parse_url(self.path)
        
        if resource == "animals":
            if id is not None:
                response = f"{get_single_animal(id)}"
            else:
                response=f"{get_all_animals()}"
        elif resource == "employees":
            if id is not None:
                response = f"{get_single_employee(id)}"
            else:
                response = f"{get_all_employees()}"
        elif resource == "locations":
            if id is not None:
                response = f"{get_single_location(id)}"
            else:
                response = f"{get_all_locations()}"
        elif resource =="customers":       
            if id is not None:
                response = f"{get_single_customer(id)}"
            else:
                response = f"{get_all_customers()}"
        # This weird code sends a response back to the client
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
    #json loads not load?    
        post_body = json.loads(post_body)
        (resource,id)=self.parse_url(self.path)
        
        new_animal = None
        new_location = None
        new_customer = None
        new_employee = None 
        
        if resource == "animals":
            new_animal = create_animal(post_body)
        self.wfile.write(f"{new_animal}".encode())

        if resource == "locations":
            new_location = create_location(post_body)
        self.wfile.write(f"{new_location}".encode())

        if resource == "customers":
            new_customer = create_customer(post_body)
        self.wfile.write(f"{new_customer}".encode())
        
        if resource =="employees":
            new_employee = create_employee(post_body)
        self.wfile.write(f"{new_employee}".encode())
    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        self.do_POST()

    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        
        if resource == "animals":
            delete_animal(id)
        elif resource == "cusomters":
            delete_customer(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "locations":
            delete_location(id)
        self.wfile.write("".encode())
        
        
# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()