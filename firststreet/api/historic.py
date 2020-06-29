# Author: Kelvin Lai <kelvin@firststreet.org>
# Copyright: This module is owned by First Street Foundation

# Standard Imports
import logging

# Internal Imports
from firststreet.api import csv_format
from firststreet.api.api import Api
from firststreet.errors import InvalidArgument
from firststreet.models.historic import HistoricEvent, HistoricSummary


class Historic(Api):
    """This class receives a list of fsids and handles the creation of a historic product from the request.

        Methods:
            get_event: Retrieves a list of Historic Event for the given list of IDs
            get_summary: Retrieves a list of Historic Summary for the given list of IDs
        """

    def get_event(self, fsids, csv=False, limit=100, output_dir=None):
        """Retrieves historic event product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Historic Event objects.

        Args:
            fsids (list/file): A First Street Foundation IDs or a file of First Street Foundation IDs
            csv (bool): To output extracted data to a csv or not
            limit (int): max number of connections to make
            output_dir (str): The output directory to save the generated csvs
        Returns:
            A list of Historic Event
        """

        # Get data from api and create objects
        api_datas = self.call_api(fsids, "historic", "event", None, limit)
        product = [HistoricEvent(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "historic", "event", output_dir=output_dir)

        logging.info("Historic Event Data Ready.")

        return product

    def get_events_by_location(self, fsids, location_type, csv=False, limit=100, output_dir=None):
        """Retrieves historic summary product data from the First Street Foundation API given a list of location
        FSIDs and returns a list of Historic Summary objects.

        Args:
            fsids (list/file): A First Street Foundation IDs or a file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            limit (int): max number of connections to make
            output_dir (str): The output directory to save the generated csvs
        Returns:
            A list of Historic Event
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")
        elif location_type == 'property':
            raise InvalidArgument("Property is not a valid location type")

        # Get data from api and create objects
        api_datas = self.call_api(fsids, "historic", "summary", location_type, limit)
        summary = [HistoricSummary(api_data) for api_data in api_datas]

        fsids = list(set([event.get("eventId") for sum_hist in summary if sum_hist.historic for
                          event in sum_hist.historic]))

        if fsids:
            api_datas_event = self.call_api(fsids, "historic", "event", None, limit)

        else:
            api_datas_event = [{"eventId": None}]

        event = [HistoricEvent(api_data) for api_data in api_datas_event]

        if csv:
            csv_format.to_csv([summary, event], "historic", "summary_event", location_type, output_dir=output_dir)

        logging.info("Historic Summary Event Data Ready.")

        return [summary, event]

    def get_summary(self, fsids, location_type, csv=False, limit=100, output_dir=None):
        """Retrieves historic summary product data from the First Street Foundation API given a list of FSIDs and
        returns a list of Historic Summary objects.

        Args:
            fsids (list/file): A First Street Foundation IDs or a file of First Street Foundation IDs
            location_type (str): The location lookup type
            csv (bool): To output extracted data to a csv or not
            limit (int): max number of connections to make
            output_dir (str): The output directory to save the generated csvs
        Returns:
            A list of Historic Summary
        Raises:
            InvalidArgument: The location provided is empty
            TypeError: The location provided is not a string
        """

        if not location_type:
            raise InvalidArgument(location_type)
        elif not isinstance(location_type, str):
            raise TypeError("location is not a string")

        # Get data from api and create objects
        api_datas = self.call_api(fsids, "historic", "summary", location_type, limit)
        product = [HistoricSummary(api_data) for api_data in api_datas]

        if csv:
            csv_format.to_csv(product, "historic", "summary", location_type, output_dir=output_dir)

        logging.info("Historic Summary Data Ready.")

        return product
