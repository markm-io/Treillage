from treillage import TreillageValidationException


class DataObject:
    def __init__(self, sectionFields: dict, data: dict):
        self._object = {}
        self._data = data
        self.sectionFields = sectionFields
        self.fieldProcess = {
            "String": self.processString,
            "Currency": self.processCurrency,
            "Percent": self.processPercent,
            "Integer": self.processInteger,
            "Text": self.processText,
            "Boolean": self.processBoolean,
            "Url": self.processUrl,
            "Date": self.processDate,
            "IncidentDate": self.processDate,
            "Dropdown": self.processDropdown,
            "PersonLink": self.processPersonLink,
            "Deadline": self.processDeadline,
            "MultiSelectList": self.processMultiSelectList,
        }
        self._dataObject = {}
        self.build()
        self.validate()

    def body(self):
        return self._object

    def validate(self):
        for key, cell in self._data.items():
            if not key.split(".")[0] in [
                field["fieldSelector"] for field in self.sectionFields
            ]:
                print(self.sectionFields)
                raise TreillageValidationException(
                    msg=f"Invalid value for {key}: {cell}."
                )

    # TODO: add additional data validation and cleanup for these field types (e.g. convert "Yes" to `true`)
    # also, the **kwargs seem to be a mess....?
    def processString(self, key, cell, **kwargs):
        self._object[key] = cell

    def processCurrency(self, key, cell, **kwargs):
        self._object[key] = cell

    def processPercent(self, key, cell, **kwargs):
        self._object[key] = cell * 100

    def processInteger(self, key, cell, **kwargs):
        self._object[key] = cell

    def processText(self, key, cell, **kwargs):
        self._object[key] = cell

    def processBoolean(self, key, cell, **kwargs):
        self._object[key] = cell

    def processUrl(self, key, cell, **kwargs):
        self._object[key] = cell

    def processDate(self, key, cell, **kwargs):
        self._object[key] = cell.strftime("%m/%d/%Y")

    def processDropdown(self, key, cell, dropdownItems, **kwargs):
        if cell in dropdownItems:
            self._object[key] = cell
        else:
            # Filevine will accept ANY string, and it will appear on reports, but will cause a glitch on the front end. This is a safety measure.
            # TO-DO: Raise an exception here, skip row, add to log.
            raise TreillageValidationException(
                msg=f"{cell} is not a valid dropdown option for {key}"
            )

    def processPersonLink(self, key, cell, **kwargs):
        # note: this will only work for NATIVE IDS as Filevine API v2 cannot handle partner IDs for person fields.
        if type(cell) == int:
            self._object[key] = {"id": cell}

    def processDeadline(self, key, cell, subKey, **kwargs):
        if not key in self._object:
            self._object[key] = {}
        if subKey == "due":
            self._object[key]["dateValue"] = cell.strftime("%m/%d/%Y")
        if subKey == "done" and cell != "":
            self._object[key]["doneDate"] = cell.strftime("%m/%d/%Y")

    def processMultiSelectList(self, key, cell, dropdownItems, **kwargs):
        if all(item in dropdownItems for item in cell.split(",")):
            self._object[key] = [item for item in cell.split(",")]
        else:
            raise TreillageValidationException(
                msg=f"{cell} is not a valid dropdown option for {key}"
            )

    def build(self):
        customFields = self.sectionFields

        for key, value in self._data.items():
            if value == "":
                continue
            if value == None:
                continue
            subKey = None
            if len(key.split(".")) > 1:
                subKey = key.split(".")[1]
            key = key.split(".")[0]
            # TO-DO: Add detection of field selector typos, etc.
            if key not in [field["fieldSelector"] for field in customFields]:
                print(f"Field selector {key} not found in section fields.")
                raise SyntaxError
            field = next(
                field for field in customFields if field["fieldSelector"] == key
            )
            fieldType = field["customFieldType"]
            dropdownItems = field["dropdownItems"]
            self.fieldProcess[fieldType](
                key, value, dropdownItems=dropdownItems, subKey=subKey
            )
