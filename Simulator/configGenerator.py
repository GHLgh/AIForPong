import ConfigParser

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
    config.add_section('DiscreteState')
    config.set('DiscreteState', 'stage_x', '12')
    config.set('DiscreteState', 'stage_y', '12')
    config.set('DiscreteState', 'velocity_x', '1')
    config.set('DiscreteState', 'velocity_y', '1')

# Writing our configuration file to 'example.cfg'
    with open('stage.cfg', 'wb') as configfile:
        config.write(configfile)
