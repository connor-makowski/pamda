import sys

class pamda_error:
    def warn(self, message, depth=0):
        """
        Usage:

        - Creates a class based warning message

        Requires:
        - `message`:
            - Type: str
            - What: The message to warn users with
            - Note: Messages with `{class_name}` and `{method_name}` in them are formatted appropriately
        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0

        Notes:

        - If `self.show_warning_stack=True`, also prints the stack trace up to 10 layers deep
        - If `self.show_warnings=False`, supresses all warnings
        """
        if self.__dict__.get('show_warnings',True):
            kwargs={
                'class_name':self.__class__.__name__,
                'method_name':sys._getframe(depth).f_back.f_code.co_name
            }
            pre_message="(Warning for `{class_name}.{method_name}`): ".format(**kwargs)
            # Attempt to format in kwargs where possible
            try:
                message=pre_message+message.format(**kwargs)
            except:
                message=pre_message+message
            if self.__dict__.get('show_warning_stack',False):
                traceback.print_stack(limit=10)
            print(message)

    def vprint(self, message, depth=0, force=False):
        """
        Usage:

        - Print a given statement if `self.verbose` is true

        Requires:

        - `message`:
            - Type: str
            - What: A message to print if `self.verbose` is true
            - Note: Messages with `{{class_name}}` and `{{method_name}}` in them are formatted appropriately

        Optional:

        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0
        - `force`:
            - Type: bool
            - What: Force a print statement even if not in verbose
            - Note: For formatting purposes
            - Default: False
        """
        if self.verbose or force:
            kwargs={
                'class_name':self.__class__.__name__,
                'method_name':sys._getframe(depth).f_back.f_code.co_name
            }
            pre_message="(`{class_name}.{method_name}`): ".format(**kwargs)
            # Attempt to format in kwargs where possible
            try:
                message=pre_message+message.format(**kwargs)
            except:
                message=pre_message+message
            print(message)

    def exception(self, message, depth=0):
        """
        Usage:

        - Creates a class based exception message

        Requires:

        - `message`:
            - Type: str
            - What: The message to warn users with
            - Note: Messages with `{{class_name}}` and `{{method_name}}` in them are formatted appropriately
        - `depth`:
            - Type: int
            - What: The depth of the nth call below the top of the method stack
            - Note: Depth starts at 0 (indicating the current method in the stack)
            - Default: 0

        Notes:

        - If `self.show_warning_stack=True`, also prints the stack trace up to 10 layers deep
        - If `self.show_warnings=False`, supresses all warnings
        """
        kwargs={
            'class_name':self.__class__.__name__,
            'method_name':sys._getframe(depth).f_back.f_code.co_name
        }
        pre_message="(Exception for `{class_name}.{method_name}`): ".format(**kwargs)
        # Attempt to format in kwargs where possible
        try:
            message=pre_message+message.format(**kwargs)
        except:
            message=pre_message+message
        raise Exception(message)
