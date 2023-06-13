# Unique (customized) impelmentation of the Alphavantage wrapper to support OpenFintech (mainly Model.test_config and Model.run_config in Model.py)

# We could potentially store the data the wrapper collects in a database/collection
# The goal would be to reduce key usage by using existing data and refreshing stored data preemptively.
# We should move the Alphavantage wrapper in here and pack it in with a new name and redesign it to suit this system (for the classes/functions mentioned above)
# We would also have to reference the wrapper in the Market component as the data for settings are esentially required by the market not the model in and of itself.