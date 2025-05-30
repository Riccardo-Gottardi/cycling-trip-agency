# Ride Descriptor
{
    ride_type: None,
    bicycle_profile: None,
    fitness_level: {
        kilometer_per_ride: 
    },
    number_of_days: 0,
    dates: [],
    locations: [],
    stepped_route: [],
    preferences: []
}

### Ride type
### bicycle profile 
- Identify the type of bike used for the trip
- Therefore influence the type of paths chosed for the ride/trip
### Fintess level
- Give information about the amout of work the user can do 
- Used to determine the daily amount of kilometers and the maximum slope for the pahts
### Number of days
### Dates
### Specified locations
### Plannded steps
- Array containing all the steps of the trip
    - a step contain all the information about the segment of the day (1 step correspond to 1 segment that correspond to 1 day)
    {
        starting_point_name: str,
        ending_point_name: str,
        starting_point_coordinates: (),
        ending_point_coordinates: (),
        route: []
    }
### Preferences



---
To start brouter

docker run --rm -v ./misc/scripts/segments4:/segments4 -v ./misc/profiles2:/profiles2 -p 17777:17777 --name brouter brouter


---

- plan_the_accommodation
Before planning the accommodation you need to have the route already planned.


---

    Use a ReAct approach. Reason on the assigned task, execute an action, observe the resolut, and repeat. 
    When asking remember that it does not have to feel like an interrogation. Try starting the conversation with a general question about the trip, and then see what is needed.

---

Conversation example 1:
You: Hi, can you tell me about the trip you are planning ?
User: Hi, sure. I'm planning a 4 day trip From Pordenone to Trieste.
You: Cool, which kind of bike do you plan to use for the trip ?
User: I have a Gravel bike.
You: Perfect, so you like to have a bit of fun off road. Can you please give me some information about your performance ? like the amount of kilometers you can do in a day, the difference in height.
User: The longest trip I've ever done was a bit more of a hundred kilometers with a different in height of a thousent and tre hundred meters.
You: Great. Do you want to give me additional information or preferences for the trip ?
User: No thank you.

Conversation example 2:
You: Hello, which trip are you planning to take ?
User: I'm planning to do a trip from Grado to Gemona with my beautiful road bike.
You: Nice, how many days do you have to dedicate to the trip ?
User: I'll have holidays from the 1st to the 3rd of june.
You: Great, nothing better than a ... to enjoy holidays. Tell me about you performance, what's the longer distance and elevation difference you can achieve in a day ?
User: For the distance, the longest ride I've done was about 80 kilometers, where for the difference in height was 2000 m
You: Perfect, are there some other informations you what to give me ?
User: Yes, I would like to go through palmanova.
You: Ok, wrote it down, Is it all ?
User: Yes man!

To understand how you should interact, here you have an example of a conversation:
context: We need to plan your cycling trip and understand your performance for the best experience.
what_to_collect: ride_type: either ONE_WAY or LOOP, bicycle_profile: type of bike used, either ROAD, GRAVEL or MTB, number_of_days: the number of days for the trip, locations: at least two locations to visit, kilometer_per_day: the maximum amount of kilometers you can ride in a day, difference_in_height_per_day: the maximum difference in height (in meters) you can handle in a day
ask_to_the_user("Hi, which trip are you planning to take ?")
User: I'm planning to do a trip from Grado to Gemona with my beautiful road bike.
ask_to_the_user(" Nice, how many days do you have to dedicate to the trip ?")
User: I'll have holidays from the 1st to the 3rd of june.
ask_to_the_user(" Great, nothing better than a ... to enjoy holidays. Tell me about you performance, what's the longer distance and elevation difference you can achieve in a day ?")
User: For the distance, the longest ride I've done was about 80 kilometers, where for the difference in height was 2000 m
ask_to_the_user(" Perfect, are there some other informations you what to give me ?")
User: Yes, I would like to go through palmanova.
ask_to_the_user(" Ok, wrote it down, Is it all ?")
User: Yes man!

---

I'm thinking of planning a 4 day trip. From Pordenone to Trieste.
I'll use a gravel bike.
A friend of mine told me that palmanova is beautiful.