#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.refinement_model import refine_thing


def create_test_data(database):
    from tracking.modelling.root_model import create_root

    # Roots
    our_test_group = create_root(name="Our Test Group", description="For testing out the code.")
    another_test_group = create_root(name="Yet Another Test Group", description="For really, really testing out the code.\nLike, a lot.")

    # Places
    metropolis = our_test_group.place.create_kind_of_place(name="Metropolis", description="Home of the Daily Planet")
    smallville = our_test_group.place.create_kind_of_place(name="Smallville", description="Superboy's Home Town.\n Also, coincidentally, childhood home of Clark Kent.")
    phone_booth = smallville.create_kind_of_place(name="Phone Booth", description="Those tall boxes that had phones back in the day.")

    # Things
    shoes = our_test_group.thing.create_kind_of_thing("Shoes", "Things to wear on your feet.")
    clothing = our_test_group.thing.create_kind_of_thing("Clothing", "Things to wear\nOr lose in the closet.")
    containers = our_test_group.thing.create_kind_of_thing("Containers", "Things to hold other things.")
    backpacks = containers.create_kind_of_thing("Backpacks", "Containers that\nStrap to your back.")
    gym_bags = containers.create_kind_of_thing("Gym Bags", description="")

    # Categories
    seasons = our_test_group.create_category("Season", "Whether for summer or winter or either.")
    sexes = our_test_group.create_category("Sex", "Whether for girl or boy or either.")
    ages = our_test_group.create_category("Age Appropriate", "Whether for infant, toddler, child, adult, or any.")

    # Choices
    winter_season = seasons.create_choice("Winter", "For when it is cold.")
    summer_season = seasons.create_choice("Summer", "For when it is warm.")
    all_season = seasons.create_choice("All Season", "For any time of year.")
    girls = sexes.create_choice("Girl's", "Specific to girls.")
    boys = sexes.create_choice("Boy's", "Specific to boys.")
    either = sexes.create_choice("Either", "Not specific to either boys or girls.")
    infant = ages.create_choice("Infant", "For 0 - 2 years old.")
    toddler = ages.create_choice("Toddler", "For 2 - 5 years old.")
    child = ages.create_choice("Child", "For 5 - 12 years old.")
    teen = ages.create_choice("Teen", "For 13 - 19 years old.")
    adult = ages.create_choice("Adult", "For adults.")

    # Refinements
    refine_thing(clothing, seasons)
    refine_thing(clothing, ages)
    refine_thing(clothing, sexes)
    refine_thing(shoes, seasons)
    refine_thing(shoes, ages)
    refine_thing(shoes, sexes)
    refine_thing(containers, seasons)
    refine_thing(backpacks, sexes)


