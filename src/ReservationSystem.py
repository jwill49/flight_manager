#! /usr/bin/env python2
# encoding=utf8

import string
import io
import re
from Flight import Flight
from Client import Client

from sys import stderr

def validate_flight(flight_info):
  '''
  Validates that flight information given is in valid format
  
  :param flight: the partitioned flight information
  :type flight: list
  '''
  if len(flight_info) != 5:
    return False
  
  flightno, capacity, price, src, dst = flight_info
  
  try:
    # I don't test if airport codes are all uppercase or not. Unspecified in assumptions, but length must be 3
    assert(re.match("^[A-z][0-9]*$", flightno) is not None)
    assert(re.match("^[0-9]*$", capacity) is not None)
    assert(re.match("^[0-9]+$|[0-9]+\.[0-9]*$", price) is not None)
    assert(re.match("^[A-z][A-z][A-z]$", src) is not None)
    assert(re.match("^[A-z][A-z][A-z]$", dst) is not None)
  except AssertionError:
    return False
  return True

class ReservationSystem:
  def __init__(self):
    self.flightno_manifest = {} # Mapping from Flightno ==> Flight
    self.route_manifest = {} # Mapping from SRC,DST ==> Flight
    self.client_manifest = {} # Mapping from name ==> Client
  
  def process_flight_manifest(self, filepath):
    '''
    Lazily process the flight manifest
    '''
    with io.open(filepath, "rtU") as f:
      print >> stderr, "Processing flight manifest from", filepath
       
      for line in f:
        flight_info = [fi.strip() for fi in string.split(line, ",")]
        
        # Validate that line follows correct format
        try:
          assert(validate_flight(flight_info))
        except AssertionError:
          print >> stderr, "Skipping:", line
          pass
        
        # Process line
        self.add_flight_to_system(flight_info)
    
    print >> stderr
    
  def process_transactions(self, filepath):
    '''
    Lazily process the transactions
    '''
    with io.open(filepath, "rtU") as f:
      print >> stderr, "Processing transactions from", filepath
      
      for line in f:
        transaction = [t.strip() for t in string.split(line, ",")]
        
        if transaction[0] == "BookPassenger":
          self.book_passenger(transaction[1], transaction[2], transaction[3])
        elif transaction[0] == "CancelPassenger":
          self.cancel_passenger(transaction[1], transaction[2], transaction[3])
        elif transaction[0] == "ChangePrice":
          self.change_price(transaction[1], transaction[2])
        else:
          print >> stderr, "Invalid transaction:", line.strip()
          pass
          
  def add_flight_to_system(self, flight_info):
    '''
    Adds a flight to the reservation system.
    
    :param flight: the partitioned flight information
    :type flight: list
    '''
    flightno, capcity, price, src, dst = flight_info
    flight = Flight(flightno, capcity, price, src, dst)
    
    self.flightno_manifest[flightno] = flight
    self.route_manifest[flight.route_key] = flight
  
  def book_passenger(self, name, src, dst):
    '''
    Books a client on a flight given name, source airport and destination.
    Returns True or False.
    
    :param name: name of flight passenger
    :type name: str or unicode
    :param src: source airport code
    :type src: str or unicode
    :param dst: destination airport code
    :type dst: str or unicode
    '''
    client = self.get_client(name)
    route_key = src + "," + dst
    
    # Does flight even exist?
    if not self.route_manifest.has_key(route_key): 
      return
    
    flight = self.route_manifest[route_key]
    client.book_flight(flight)
  
  def cancel_passenger(self, name, src, dst):
    '''
    Cancels a flight for a passenger on a flight given name, source airport and destination.
    Returns True or False.
    
    :param name: name of flight passenger
    :type name: str or unicode
    :param src: source airport code
    :type src: str or unicode
    :param dst: destination airport code
    :type dst: str or unicode
    '''
    client = self.get_client(name)
    route_key = src + "," + dst
    
    # Does flight even exist?
    if not self.route_manifest.has_key(route_key): 
      return
    
    flight = self.route_manifest[route_key]
    number_of_flights = client.cancel_flight(flight)
    
    # Client has no remaining flights in itinerary. For space concerns, remove from working memory
    if number_of_flights == 0:
      del self.client_manifest[client.name]
      del client
  
  def change_price(self, flightno, price):
    '''
    Changes the price for a given flight
    
    :param flightno: the flight number
    :type flightno: str or unicode
    :param price: price of the flight
    :type price: str or unicode
    '''
    try:
      assert(re.match("^[0-9]+$|[0-9]+\.[0-9]*$", price) is not None)
    except AssertionError:
      print >> stderr, price, "is in wrong format"
      return
    
    flight = self.flightno_manifest[flightno]
    flight.change_price(price)
  
  def get_client(self, name):
    '''
    Returns the Client that corresponds to the given name or creates a new one if he/she doesn't exist.
    
    :param name: name of flight passenger
    :type name: str or unicode
    '''
    if self.client_manifest.has_key(name):
      return self.client_manifest[name]
    
    client = Client(name)
    self.client_manifest[name] = client
    return client
    
  def output_to_txt(self, filepath):
    """
    Outputs system state to a file
    
    :param filepath: path of desired output file
    :type filepath: str or unicode
    """
    total_seats_sold = 0
    total_revenue = 0.0
    fmt = "{0:20}{1:8}{2:6}"
    
    with io.open(filepath, "wb") as file:
      for flight in self.flightno_manifest.values():
        total_seats_sold += len(flight.passenger_manifest)
        total_revenue += flight.revenue
        
        print >> file, flight
        
      print >> file,"System’s summary:"
      print >> file, "Total Seats Sold:", total_seats_sold
      print >> file, "Total Revenue:", "$" + str(total_revenue)

if __name__ == '__main__':
  flight_manifest_path = "in/inputfile1.txt"
  transactions_path = "in/inputfile2.txt"
  output_path = "out/output.txt"
  
  rs = ReservationSystem()
  rs.process_flight_manifest(flight_manifest_path)
  rs.process_transactions(transactions_path)
  rs.output_to_txt(output_path)