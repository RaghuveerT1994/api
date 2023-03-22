import json
import logging
from django.db.models.query_utils import Q
from datetime import datetime

from connection.models import ConnectionHistory
from connection.serializers import ConnectionHistoryListSerializer, ConnectionHistorySerializer

from deepdiff import DeepDiff

# Get an instance of a logging
log = logging.getLogger(__name__)

class HistoryController:

    def history_create(self, connection_id, user_id, table_name, history_status, description, changed_attributes = '' ):
        try:
            history_data = {}
            if description and history_status and table_name:
                history_data['connection_id'] = connection_id
                history_data['changed_attributes'] =  ''
                if changed_attributes:
                    history_data['changed_attributes'] = json.dumps(str(changed_attributes))
                history_data['table_name'] = table_name
                history_data['history_status'] = history_status
                history_data['description'] = description
                history_data['created_by'] = user_id
                history_data['created_date'] = datetime.now()
                history_save = ConnectionHistorySerializer(data = history_data)
                if history_save.is_valid():
                    inserted_id = history_save.save()
                else:
                    log.info(history_save.errors)

            else:
                 log.info("No data found in history")

        except Exception as e:
            print(str(e))
            return ''

    def history_data_format(self, values_changed, requestData, user_id, table_name, connection_id, name):
        try:
            for key in values_changed:
                history_status = ''
                if "iterable_item_removed" == key:
                    history_status = name + " was modified"
                    for mapping in values_changed[key]: 
                        msgs = ''
                        design = values_changed[key][mapping].items()
                        for key3, value3 in design:
                            if value3:
                                msgs += key3+ " is " + value3
                                msgs = msgs + ", "
                        if msgs:
                            description = "Value removed from {}".format(msgs)
                            description = description[:-2]
                            self.history_create(connection_id,user_id, table_name, history_status, description,  changed_attributes =values_changed)
                elif "iterable_item_added" == key:
                    history_status = name + " was modified"
                    for mapping in values_changed[key]: 
                        msg = ''
                        design = values_changed[key][mapping].items()
                        for key1, value1 in design:
                            if value1:
                                msg += key1+ " is " + value1
                                msg = msg + ", "
                        if msg:
                            description = "Values added to {}".format(msg)
                            description = description[:-2]
                            self.history_create(connection_id, user_id, table_name, history_status, description ,  changed_attributes =values_changed)
                elif "values_changed" == key:
                    history_status = name + " was modified"
                    message = ''
                    column_name = values_changed[key]
                    for key2 in column_name:
                        spl = key2.split('[')[-1].split(']')[0]
                        if spl != "'parameter'":
                            message += spl + " has changed from " + str(column_name[key2]['old_value']) + " to " +  str(column_name[key2]['new_value'])
                            if list(column_name.keys())[-1] != key2:
                                message = message + ", "
                        else:
                            self.parameter_history(name, connection_id, column_name[key2]['new_value'], user_id, old_data=column_name[key2]['old_value'])
                        if message:
                            description = "Values changed in {}".format(message)
                    if description:
                        self.history_create(connection_id, user_id, table_name, history_status, description,  changed_attributes =values_changed)
            
        except Exception as e:
            print(str(e))
            return ''

    def parameter_history(self, name, connection_id, connection_data, user_id, old_data=''):
        try:
            connection_data = json.loads(connection_data)
            old_data = json.loads(old_data)
            if old_data:
                if old_data and connection_data:
                    parameter_history = DeepDiff(old_data,connection_data, ignore_order = True, report_repetition=True, ignore_type_in_groups=[(str, bytes, datetime)])

                    for key in parameter_history:
                        if "values_changed" == key:
                            history_status = name + " was modified"
                            message = ''
                            column_name = parameter_history[key]
                            for key1 in column_name:
                                spl = key1.split('[')[-1].split(']')[0]
                                message += spl + " has changed from " + str(column_name[key1]['old_value']) + " to " +  str(column_name[key1]['new_value'])
                                if list(column_name.keys())[-1] != key1:
                                    message = message + ", "
                            description = "Values changed in {}".format(message)
                            self.history_create(connection_id, user_id, "connection", history_status, description,  changed_attributes =parameter_history)
                
        except Exception as e:
            print(str(e))
            return ''
           
    def grouping(self, connection_id, filter_value = 0):
        try:
            total_count = 0
            condition = Q(connection_id= connection_id)
            if filter_value:
                or_condition = Q(table_name__icontains = filter_value)
                or_condition.add(Q(history_status__icontains = filter_value), Q.OR)
                or_condition.add(Q(description__icontains = filter_value), Q.OR)
                condition &= or_condition

            response = ConnectionHistory.objects.filter(condition).order_by('-created_date')

            total_count = ConnectionHistory.objects.filter(condition).count()
            serializer = ConnectionHistoryListSerializer(response, many=True)
            date_arr = []
            format_arr = {}
            result = {}
            result['count'] = total_count
            # Seperate date wise. 
            for i in serializer.data:
                date = datetime.strptime(i["created_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                date = date.strftime("%Y-%m-%d")
                if not date in date_arr:
                    date_arr.append(date)
                    format_arr[date]= [i]
                else:
                    format_arr[date].append(i)
            result['data'] = format_arr
            return result

        except Exception as e:
            print(str(e))
            return False