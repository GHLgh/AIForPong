import ConfigParser

if __name__ == "__main__":
    onfig = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
    config.add_section('DiscreteState')
    config.set('DiscreteState', 'an_int', '15')
    config.set('DiscreteState', 'a_bool', 'true')
    config.set('DiscreteState', 'a_float', '3.1415')
    config.set('DiscreteState', 'baz', 'fun')
    config.set('DiscreteState', 'bar', 'Python')
    config.set('DiscreteState', 'foo', '%(bar)s is %(baz)s!')

# Writing our configuration file to 'example.cfg'
with open('example.cfg', 'wb') as configfile:
    config.write(configfile)
