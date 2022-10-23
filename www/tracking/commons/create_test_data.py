#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.particular_thing_model import find_or_create_particular_thing
from tracking.modelling.postioning_model import add_quantity_of_things
from tracking.modelling.refinement_model import add_refinement


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

    # Particulars
    girls_winter_clothing = find_or_create_particular_thing(clothing, [winter_season, girls])
    girls_summer_clothing = find_or_create_particular_thing(clothing, [summer_season, girls])
    toddler_summer_clothing = find_or_create_particular_thing(clothing, [summer_season, toddler])
    mens_clothing = find_or_create_particular_thing(clothing, [boys, adult])
    either_child_clothing = find_or_create_particular_thing(clothing, [either, child])
    generic_clothing = clothing.generic

    boys_backpacks = find_or_create_particular_thing(backpacks, [boys])
    girls_backpacks = find_or_create_particular_thing(backpacks, [girls])

    # Positioning
    add_quantity_of_things(smallville, either_child_clothing, 2)
    add_quantity_of_things(phone_booth, mens_clothing, 3)
    add_quantity_of_things(smallville, girls_winter_clothing, 5)
    add_quantity_of_things(smallville, girls_summer_clothing, 8)
    add_quantity_of_things(metropolis, girls_winter_clothing, 13)
    add_quantity_of_things(metropolis, toddler_summer_clothing, 21)
    add_quantity_of_things(metropolis, generic_clothing, 34)
    add_quantity_of_things(smallville, boys_backpacks, 55)
    add_quantity_of_things(smallville, girls_backpacks, 89)



