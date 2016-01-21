# Run a test server.
from app import app

# Import config parser to load IP and port settings
import ConfigParser

# Get settings for running server - these should be stored in a config.ini file
parser = ConfigParser.SafeConfigParser()
parser.read('config.ini')
host_ip = parser.get('Host Config', 'ip')
host_port = parser.getint('Host Config', 'port')
debug_config = parser.getboolean('Host Config', 'debug')

# Run the server
app.run(host=host_ip, port=host_port, debug=debug_config)
