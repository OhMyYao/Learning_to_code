import sys

class Customer:
    '''A superclass as template for different retail and wholesale customer subclasses'''
    __id = None
    __name = None

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        if value == None:
            raise ValueError("ID cannot be None")
        elif not isinstance(value,str):
            raise ValueError("ID needs to be letters")
        elif len(value.strip())<=0:
            raise ValueError("ID cannot be blank")
        self.__id = value.strip()
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,value):
        if value == None:
            raise ValueError("Name cannot be None")
        elif not isinstance(value,str):
            raise ValueError("Name needs to be letters")
        elif len(value.strip())<=0:
            raise ValueError("Name cannot be blank")
        self.__name = value.strip()

    def get_discount(self, price):
        pass

class RetailCustomer(Customer):
    __rate = None
    '''Retail Customer class based off the customer class to determine rates and id'''
    def __init__(self, id, name, rate):
        self.rate = rate
        super().__init__(id, name)

    @property
    def rate(self):
        return self.__rate
    
    @rate.setter
    def rate(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Rate must be a number.")
        elif not (0 <= value <= 1):
            raise ValueError("Rate must be between 0 and 1.")
        self.__rate = value

    def get_discount(self, price):
        return price * (1 - self.rate)
    
    def displayCustomer(self):
        sys.stdout.write(f"Customer: {self.name}\nID: {self.id}\nDiscount Rate: {self.rate * 100}%\n")


class WholesaleCustomer(Customer):
    '''Wholesale customer class based off the customer class with different rates depending on purchase amount'''
    __rate1 = None
    __rate2 = None

    def __init__(self, id, name, rate1, rate2):
        self.rate1 = rate1
        self.rate2 = rate2
        super().__init__(id, name)

    @property
    def rate1(self):
        return self.__rate1
    
    @property
    def rate2(self):
        return self.__rate2
    
    @rate1.setter
    def rate1(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Rate must be a number.")
        elif not (0 <= value <= 1):
            raise ValueError("Rate must be between 0 and 1).")
        self.__rate1 = value

    @rate2.setter
    def rate2(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Rate must be a number.")
        elif not (0 <= value <= 1):
            raise ValueError("Rate must be between 0 and 1).")
        self.__rate2 = value

    def get_discount(self, price):
        '''Returning the discounted rate depending on amount spent'''
        if price <= 1000:
            return price * (1 - self.rate1)
        elif price > 1000:
            return price * (1 - self.rate2)
    
    def displayCustomer(self):
        sys.stdout.write(f"Customer: {self.name}\nID: {self.id}\nDiscount Rate1: {self.rate1 * 100}%\nDiscount Rate2: {self.rate2 * 100}%\n")

#----------------

class PartShortException(Exception):
    '''Exception for when required parts exceed maximum number that can be supplied'''
    pass

#----------------

class Part:
    def __init__(self, ID, name, price, total):
        self.__ID = ID
        self.__name = name
        self.__price = price
        self.__total = total

    @property
    def name(self):
        return self.__name
    
    @property
    def total(self):
        return self.__total
    
    @property
    def ID(self):
        return self.__ID
    
    @property
    def price(self):
        return self.__price

    def replenish(self, amount):
        if not isinstance(amount, int):
            raise ValueError("Amount must be a number.")
        elif amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        self.__total += amount
        
    def supply(self, amount):
        if not isinstance(amount, int):
            raise ValueError("Amount must be a number.")
        elif amount > self.__total:
            raise PartShortException("Amount exceeds total available.")
        self.__total -= amount


class AssembledPart(Part):
    def __init__(self, ID, name, price, CP1, CP2, total):
        super().__init__(ID, name, price, total)
        self.__CP1 = CP1
        self.__CP2 = CP2

    @property
    def CP1(self):
        return self.__CP1
    
    @property
    def CP2(self):
        return self.__CP2

#----------------

class WarehouseManager:
    def __init__(self):
        self.customers = []
        self.parts = []

    def readCustomers(self, file_name):
        try:
            with open(file_name, "r") as i:
                for line in i:
                    fields = line.split(",")
                    if len(fields) == 3:
                        #will check if it's a retail customer, and if so will seperate into the customer fields
                        part = RetailCustomer(fields[0], fields[1], float(fields[2]))
                        self.customers.append(part)

                    elif len(fields) == 4:
                        #Checks if it's a wholesale customer which has 4 components
                        part = WholesaleCustomer(fields[0], fields[1], float(fields[2]), float(fields[3]))
                        self.customers.append(part)
        except Exception:
            print(f"Issue occurred while opening {file_name}")

    def readParts(self, file_name):
        try:
            with open(file_name, "r") as i:
                for line in i:
                    fields = line.strip().split(",")
                    if len(fields) == 4:
                        #will check if there are 4 components, and if so will seperate into components
                        part = Part(fields[0], fields[1], float(fields[2]), int(fields[3]))
                        self.parts.append(part)

                    elif len(fields) == 6:
                        #Checks if it's a assembledpart which has 6 components
                        part = AssembledPart(fields[0], fields[1], float(fields[2]), fields[3], fields[4], int(fields[5]))
                        self.parts.append(part)
        except Exception:
            print(f"Issue occurred while opening {file_name}")

    def findPart(self, id):
        for i in self.parts:
            if i.ID == id:
                return i
        return None
            
    def findCustomer(self, id):
        for i in self.customers:
            if i.id == id:
                return i
        return None

    def displayParts(self):
        sys.stdout.write("The parts that are available are:\n")
        for i in self.parts:
            sys.stdout.write(f"ID: {i.ID}, Name: {i.name}, Price: {i.price}, No. available: {i.total}\n")

    def displayCustomers(self):
        sys.stdout.write("This is the customer list:\n")
        for i in self.customers:
            i.displayCustomer()

#----------------

class WarehouseManagerUI:  
    warehousemanager = WarehouseManager()

    def run_warehouse_manager(self):
        customer_file_name = "customers.txt"
        parts_file_name = "parts.txt"
        if (self.warehousemanager.readCustomers(customer_file_name)==None):
            sys.stdout.write("Could not load file: "+customer_file_name)
        if (self.warehousemanager.readParts(parts_file_name)==None):
            sys.stdout.write("Could not load file: "+parts_file_name)
        
        choice = self.get_menu_choice()
        while (choice != "q"):
            sys.stdout.write("\n")
            if (choice=="r"):
                self.replenish()
            elif (choice=="s"):
                self.supply()
            elif (choice=="a"):
                self.assemble()
            elif (choice=="d"):
                self.warehousemanager.displayParts()
            elif (choice=="c"):
                self.warehousemanager.displayCustomers()
            choice = self.get_menu_choice()

    def get_menu_choice(self):
        menu="\n===================\n"
        menu+="Warehouse Manager \n"
        menu+="[R]eplenish a part \n"
        menu+="[S]upply a part \n"
        menu+="[A]ssemble a part \n"
        menu+="[D]isplay all parts \n"
        menu+="Display all [C]ustomers \n"
        menu+="[Q]uit \n"
        
        sys.stdout.write(menu)
        menu=menu.lower()
        choice=self.get_str("Enter choice: ").lower()
        while not "["+choice+"]" in menu:
            choice = self.get_str(choice+" was an invalid choice! Re-enter:").lower()
        return choice
    
    def get_str(self, prompt):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        value = sys.stdin.readline().strip()
        while (len(value)==0):
            sys.stdout.write("Input cannot be blank. Re-enter:")
            sys.stdout.flush()
            value = sys.stdin.readline().strip()
        return value
    
    def get_int(self, prompt):
        value=None
        while (value==None):
            try:
                value = int(self.get_str(prompt))
            except:
                sys.stdout.write("Please enter an integer.\n")
                sys.stdout.flush()
        return value
    
    def get_id(self):
        #Checking if ID provided by user is within the database. To be reused in later methods.
        id = self.get_str("Please enter the ID of the part you want: \n").strip()
        sys.stdout.flush()
        while self.warehousemanager.findPart(id) == None:
            id = self.get_str("Part ID not found. Please try again: \n").strip()
            sys.stdout.flush()
        return id

    def replenish(self):
        id = self.get_id()
        part = self.warehousemanager.findPart(id)
        amount = self.get_int("How much are you restocking? \n")
        sys.stdout.flush()
        part.replenish(amount)
        sys.stdout.write(f"Part {id} has been replenished by {amount}.\n")
            
    def supply(self):
        id = self.get_id()
        part = self.warehousemanager.findPart(id)
        
        while True:
            amount = self.get_int("How many do you need?")
            sys.stdout.flush()
            if amount > part.total:
                raise PartShortException(f"Not enough parts of {part.ID} available. Only {part.total} available.\n")
            else:
                break

        customer = None       
        while customer == None:
            customerID = self.get_str("What is the customer ID? \n").strip()
            customer = self.warehousemanager.findCustomer(customerID)
            if customer == None:
                sys.stdout.write(f"Customer ID {customerID} not found\n")
        
        subtotal = part.price * amount
        total = customer.get_discount(subtotal)
        sys.stdout.write(f"Your total comes to {total}\n")

        part.supply(amount)
        sys.stdout.write(f"Supplied {amount} of part {part.ID}\n")

    def assemble(self):
        sys.stdout.write("You have chosen to assemble parts. Please enter the ID of the items.\n")
        assembledPartID = self.get_id()
        assembledPart = self.warehousemanager.findPart(assembledPartID)

        if not isinstance(assembledPart, AssembledPart):
            sys.stdout.write("The selected part is not an assembled part.\n")
            return

        cp1_id = assembledPart.CP1
        cp2_id = assembledPart.CP2

        #finding the components for the assembly of parts
        cp1 = self.warehousemanager.findPart(cp1_id)
        cp2 = self.warehousemanager.findPart(cp2_id)

        if cp1 == None or cp2 == None:
            sys.stdout.write("One or Both of the components could not be found.\n")
            return
        
        if cp1.total < 1 or cp2.total < 1:
            raise PartShortException(f"Not enough quantity to assemble part {assembledPart.ID} {assembledPart.name}.")
        
        cp1.supply(1)
        cp2.supply(1)
        assembledPart.replenish(1)
        sys.stdout.write(f"Assembled 1 unit of {assembledPart.ID} ({assembledPart.name}).\n")


##Testing application
warehousemanagerUI = WarehouseManagerUI()
warehousemanagerUI.run_warehouse_manager()