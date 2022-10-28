#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.postioning_model import add_quantity_of_things
from tracking.modelling.refinement_model import add_refinement


def create_test_data(database):
    from tracking.modelling.root_model import create_root

    # Roots
    our_test_group = create_root(name="Our Test Group", description="For testing out the code.")
    another_test_group = create_root(name="Yet Another Test Group",
                                     description="For really, really testing out the code.\nLike, a lot.")

    # Places
    metropolis = our_test_group.place.create_kind_of_place(name="Metropolis", description="Home of the Daily Planet")
    smallville = our_test_group.place.create_kind_of_place(name="Smallville",
                                                           description="Superboy's Home Town.\n Also, coincidentally, "
                                                                       "childhood home of Clark Kent.")
    phone_booth = smallville.create_kind_of_place(name="Phone Booth",
                                                  description="Those tall boxes that had phones back in the day.")

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
    either = sexes.create_choice("Either Sex", "Not specific to either boys or girls.")
    infant = ages.create_choice("Infant", "For 0 - 2 years old.")
    toddler = ages.create_choice("Toddler", "For 2 - 5 years old.")
    child = ages.create_choice("Child", "For 5 - 12 years old.")
    teen = ages.create_choice("Teen", "For 13 - 19 years old.")
    adult = ages.create_choice("Adult", "For adults.")

    # Refinements
    add_refinement(clothing, seasons)
    add_refinement(clothing, ages)
    add_refinement(clothing, sexes)
    add_refinement(shoes, seasons)
    add_refinement(shoes, ages)
    add_refinement(shoes, sexes)
    add_refinement(containers, seasons)
    add_refinement(backpacks, sexes)

    # Specifications
    girls_specification = our_test_group.find_or_create_specification([girls])
    boys_specification = our_test_group.find_or_create_specification([boys])
    girls_winter_specification = our_test_group.find_or_create_specification([winter_season, girls])
    girls_summer_specification = our_test_group.find_or_create_specification([summer_season, girls])
    toddler_summer_specification = our_test_group.find_or_create_specification([summer_season, toddler])
    mens_specification = our_test_group.find_or_create_specification([boys, adult])
    either_child_specification = our_test_group.find_or_create_specification([either, child])
    generic_specification = our_test_group.find_or_create_specification([])

    # Positioning
    add_quantity_of_things(smallville, clothing, either_child_specification, 2)
    add_quantity_of_things(phone_booth, clothing, mens_specification, 3)
    add_quantity_of_things(smallville, clothing, girls_winter_specification, 5)
    add_quantity_of_things(smallville, clothing, girls_summer_specification, 8)
    add_quantity_of_things(metropolis, clothing, girls_winter_specification, 13)
    add_quantity_of_things(metropolis, clothing, toddler_summer_specification, 21)
    add_quantity_of_things(metropolis, clothing, generic_specification, 34)
    add_quantity_of_things(smallville, backpacks, boys_specification, 55)
    add_quantity_of_things(smallville, backpacks, girls_specification, 89)
    add_quantity_of_things(smallville, backpacks, boys_specification, 55)
    add_quantity_of_things(smallville, gym_bags, girls_specification, 10)
