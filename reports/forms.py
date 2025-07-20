# forms.py
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={
                "class": "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": "Enter your username or email",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": "******************",
                "required": True,
            }
        ),
    )

    # Add this method to add error class dynamically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (
                    f"{existing_classes} border-red-500".strip()
                )  # Add error class
            # Ensure base classes are present even without errors
            else:
                base_classes = "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                existing_classes = field.widget.attrs.get("class", "")
                # Avoid duplicating base classes if they were already set
                if base_classes not in existing_classes:
                    field.widget.attrs["class"] = (
                        f"{existing_classes} {base_classes}".strip()
                    )


class SignupForm(forms.Form):
    email = forms.CharField(
        label="Email Address",
        widget=forms.TextInput(
            attrs={
                "class": "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": "Enter your email",
                "required": True,
                "type": "email",
            }
        ),
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": "Enter your username",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": "******************",
                "required": True,
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "placeholder": "******************",
                "required": True,
            }
        ),
    )

    # Add this method to add error class dynamically
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                existing_classes = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = (
                    f"{existing_classes} border-red-500".strip()
                )  # Add error class
            # Ensure base classes are present even without errors
            else:
                base_classes = "shadow-sm appearance-none border rounded-md w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                existing_classes = field.widget.attrs.get("class", "")
                # Avoid duplicating base classes if they were already set
                if base_classes not in existing_classes:
                    field.widget.attrs["class"] = (
                        f"{existing_classes} {base_classes}".strip()
                    )
