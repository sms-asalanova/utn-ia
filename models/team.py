from models.city import City

class Team:
    def __init__(self,name,size,binary_id,last_match,total_distance_traveled,city: City):
        self.id = 0
        self.name = name
        self.size = size
        #binary_id is deprecated
        self.binary_id = binary_id
        self.last_match = last_match
        self.total_distance_traveled = total_distance_traveled
        self.city = city

    def __repr__(self):
      return self.name

    def set_team_id(self,team_id):
        self.id = team_id


    def set_city(self,city):
        self.city = city
    
    def set_last_match(self,last_match):
        self.last_match = last_match
    
    def set_total_distance_traveled(self,distance_traveled):
        self.total_distance_traveled = distance_traveled