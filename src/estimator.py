def calculateEstimate(data, converted_time, type='impact'):
    my_dict= {}
    # calculate factor value
    factor = 2 ** (converted_time // 3)
    # my solution  for challenge one
    if type == 'impact':
        my_dict['currentlyInfected'] = int(my_dict['reportedCases'] * 10)
        my_dict['infectionsByRequestedTime'] = my_dict['currentlyInfected'] * factor
    elif type == 'severeImpact':
        my_dict['currentlyInfected'] = int(data['reportedCases'] * 50)
        my_dict['infectionsByRequestedTime'] = int(
            my_dict['currentlyInfected'] * factor)
    # my solution for challenge two
    my_dict['severeCasesByRequestedTime'] = int(
        0.15 * my_dict['infectionsByRequestedTime'])
    available_beds = 0.35 * data['totalHospitalBeds']
    my_dict['hospitalBedsByRequestedTime'] = int(
        available_beds - my_dict['severeCasesByRequestedTime'])
    # my solution for challenge three
    my_dict['casesForICUByRequestedTime'] = int(0.05 * my_dict['infectionsByRequestedTime'])
    my_dict['casesForVentilatorsByRequestedTime'] = int(0.02 * my_dict['infectionsByRequestedTime'])
    dollars_in_flight = my_dict['infectionsByRequestedTime'] * data['region']['avgDailyIncomePopulation'] * \
        data['region']['avgDailyIncomeInUSD']
    my_dict['dollarsInFlight'] = int(dollars_in_flight / converted_time)
    return my_dict


def estimator(data):
    # convert time
    converted_time = data['timeToElapse']
    if data['periodType'] == 'weeks':
        converted_time = converted_time * 7
    elif data['periodType'] == 'months':
        converted_time = converted_time * 30
    impact = calculateEstimate(data, converted_time=converted_time)
    severe_impact = calculateEstimate(
        data, converted_time=converted_time, type='severeImpact')
    result = {
        'data': data,
        'impact': impact,
        'severeImpact': severe_impact
    }
    return result 