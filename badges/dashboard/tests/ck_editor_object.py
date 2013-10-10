from selenium.webdriver.remote.command import Command


class Ckeditor(object):
    ## Constructor.
    #
    # @param webelement The span or div webelement containing the ckeditor field.
    def __init__(self, webelement):
        self.element = webelement
        # Strip 'cke_' to get the CKEditor instance id.
        self.id = webelement.get_attribute('id')[4:]

    # Execute a command against CKEditor.
    def execute(self, method, *args):
        if len(args) > 0:
            converted_args = "'" + "', '".join(args) + "'"
        else:
            converted_args = ''
        script = "return CKEDITOR.instances['%s'].%s(%s);" % (self.id, method, converted_args)
        print script
        return self.element._execute(Command.EXECUTE_SCRIPT, {'script': script})['value']

    # Clear the field.
    def clear(self):
        return self.execute('setData', '')

    # Enter a value into the field.
    def send_keys(self, value):
        return self.execute('setData', value)

    # Retrieve the current value of the field
    @property
    def text(self):
        return self.execute('getData')
