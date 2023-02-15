from typing import List, Dict
from .. import TreillageValidationException


class Contact:
    def __init__(
        self,
        metadata: List[dict],
        firstName: str = "",
        middleName: str = "",
        lastName: str = "",
        nickname: str = "",
        prefix: str = "",
        suffix: str = "",
        fromCompany: str = "",
        jobTitle: str = "",
        department: str = "",
        isSingleName: bool = "",
        isArchived: bool = "",
        isDeceased: bool = "",
        birthdate: str = "",
        deathdate: str = "",
        addresses: List[dict] = [],
        phones: List[dict] = [],
        emails: List[dict] = [],
        personTypes: List[str] = [],
        hashtags: List[str] = [],
        customFields: dict = {},
    ):
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.nickname = nickname
        self.prefix = prefix
        self.suffix = suffix
        self.fromCompany = fromCompany
        self.jobTitle = jobTitle
        self.department = department
        self.isSingleName = isSingleName
        self.isArchived = isArchived
        self.isDeceased = isDeceased
        self.birthdate = birthdate
        self.deathdate = deathdate
        self.addresses = addresses
        self.phones = phones
        self.emails = emails
        self.personTypes = personTypes
        self.addresses = addresses
        self.hashtags = hashtags
        self.customFields = customFields
        self.metadata = metadata

    def build_body_custom(self):
        arguments = [x for x in vars(self).items()]

        body = list()

        def addAction(key, action, value):
            body.append({"selector": key, "action": action, "value": value})

        standardStringFields = "firstName middleName lastName nickname prefix suffix fromCompany jobTitle department birthdate deathdate".split()
        standardBoolFields = "isSingleName isArchived isDeceased".split()
        addressFields = (
            "line1 line2 city state zip notes addressLabel addressLabelID".split()
        )
        phoneFields = "number notes phoneLabel phoneLabelID".split()
        emailFields = "address notes emailLabel emailLabelId".split()

        def processCustomFields():
            for key, value in self.customFields.items():
                if value is None or value == "":
                    continue
                try:
                    field = next(x for x in self.metadata if x["selector"] == key)
                    action = next(
                        iter(
                            field["action"].split("|")
                        )  # "action": "UPDATE|REMOVE" / "actions": "ADD|REMOVE"
                    )
                    if field.get("allowedValues"):
                        allowedValues = field["allowedValues"]
                        if value not in allowedValues:
                            raise TreillageValidationException(
                                f"{value} is an invalid value for {key}. Allowed values are {allowedValues}"
                            )
                    addAction(key, action, value)
                except:
                    raise TreillageValidationException(
                        f"Invalid custom field: {key}={value}"
                    )

        def processAddressEmailPhone(key, value, fields):
            if not isinstance(value, List):
                raise TreillageValidationException(f"{key} must be a list.")

            for item in value:

                if not isinstance(item, Dict):
                    raise TreillageValidationException(
                        f"'{key}' must be a list of dictionaries"
                    )

                if not set(item.keys()).issubset(fields):
                    raise TreillageValidationException(
                        f"{key} includes invalid fields:" + f"{item.keys()}"
                    )

                if item.get("state"):
                    if len(item["state"]) > 2:
                        raise TreillageValidationException(
                            f"State field cannot be > 2 characters: " + item["state"]
                        )
                if self.metadata:

                    mode = (
                        "address"
                        if key == "addresses"
                        else "phone"
                        if key == "phones"
                        else "email"
                    )
                    labelAllowedValues = next(
                        item for item in self.metadata if item["selector"] == key
                    )["allowedValues"]

                    labelIdKey = f"{mode}LabelID"
                    labelKey = f"{mode}Label"

                    """
                    # removing this because I never want to map a label to a labelID
                    # validate LabelID if provided
                    if item.get(labelIdKey):
                        if not item[labelIdKey] in [
                            x[labelIdKey] for x in labelAllowedValues
                        ]:
                            raise TreillageValidationException(
                                labelIdKey + " is not valid: " + item[labelIdKey]
                            )
                    """
                    # Replace label with labelID
                    if item.get(labelKey):
                        if item[labelKey] in [x["name"] for x in labelAllowedValues]:
                            item[labelIdKey] = next(
                                x
                                for x in labelAllowedValues
                                if x["name"] == item[labelKey]
                            )[labelIdKey]
                            del item[labelKey]
                        else:
                            invalidLabel = item[labelKey]
                            raise TreillageValidationException(
                                f"{mode} label is not valid: {invalidLabel}"
                            )
                    # if address/phone/email passed validation, add it to the body
                    print(mode, labelKey, item)
                print("action:", key, item)
                addAction(key, "ADD", item)

        # Begin processing arguments:

        for key, value in arguments:

            if key in standardStringFields and value:
                addAction(key, "UPDATE", value)

            if key in standardBoolFields:
                if value is None or value == "":  # IMPORTANT for PATCH requests
                    continue
                if isinstance(value, bool):
                    addAction(key, "UPDATE", value)
                else:
                    raise TreillageValidationException(f"{key}: {value} is not a bool")

            if key == "hashtags" and value:
                try:
                    tags = value.split(", ")
                    for tag in tags:
                        addAction("hashtags", "ADD", tag)
                except:
                    raise TreillageValidationException(f"Invalid hashtags: {value}")

            if key == "addresses" and value:
                processAddressEmailPhone(key, value, addressFields)

            if key == "phones" and value:
                processAddressEmailPhone(key, value, phoneFields)

            if key == "emails" and value:
                processAddressEmailPhone(key, value, emailFields)

            if key == "personTypes" and value:
                personTypes = value.split(", ")
                allowedTypes = next(
                    item for item in self.metadata if item["selector"] == key
                )["allowedValues"]
                for personType in personTypes:
                    try:
                        id = next(x for x in allowedTypes if x["name"] == personType)[
                            "value"
                        ]
                    except:
                        raise TreillageValidationException(
                            f"Invalid personType: {personType}"
                        )
                    addAction(key, "ADD", id)
        processCustomFields()
        return body
