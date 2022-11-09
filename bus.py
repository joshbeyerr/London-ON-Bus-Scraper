import time

import requests
from datetime import datetime

session = requests.Session()

def printNicely(whatDate, businfo):

    print('\n\n\n')
    print('ALL AVAILABLE BUSSES FOR: {}'.format(whatDate))

    for x in businfo:
        print('')
        time.sleep(1)
        if not businfo[x]:
            print('We Are Very Sorry, There are No Busses Available For {}'.format(x))
            time.sleep(1)
        else:
            print(' ')
            print('Bus Company: {}\n'.format(x))
            counter = 1
            for i in businfo[x]:
                time.sleep(0.5)
                print('{} Option {}: '.format(x, counter))
                for j in i:
                    print('{}: {}'.format(j, i[j]))
                    time.sleep(0.5)

                counter += 1
                for xxx in range(10):

                    print('- ', end='')
                    time.sleep(0.15)
                print('')
            print('\n')



def getTime(timee):
    if 'T' in timee:
        splitTime = timee.split('T')
        if '-' in splitTime[1]:
            splittingTime = splitTime[1].split('-')
            return splittingTime[0]

        else:
            return splitTime[1]

    else:
        return timee


def getBus(userDate):
    monitor = True
    while monitor:

        date = userDate
        datesplit = userDate.split('-')
        year = datesplit[0]
        month = datesplit[1]
        day = datesplit[2]


        allBus = {'Megabus': [], 'OnexBus': [], 'FlixBus': []}

        # MegaBus

        megaBus = requests.get(
            'https://ca.megabus.com/journey-planner/api/journeys?originId=571&destinationId=145&departureDate={}'
            '&totalPassengers=1&concessionCount=0&nusCount=0&otherDisabilityCount=0&wheelchairSeated=0&pcaCount=0'
            '&days=1'.format(date))

        megaJson = megaBus.json()

        if megaJson['journeys']:
            allJourneys = megaJson['journeys']

            for x in allJourneys:
                departure = x['departureDateTime']
                departureTime = getTime(departure)
                arrival = x['arrivalDateTime']
                arrivalTime = getTime(arrival)
                price = x['price']
                stock = x['lowStockCount']
                if stock == 'null' or stock is None:
                    stock = 'Good Enough'

                allBus['Megabus'].append({"departureTime": departureTime, "arrivalTime": arrivalTime, "Price": price,
                                          "stockLevels": stock})

        # Onex Bus

        onexBus = requests.get(
            'https://api.betterez.com/inventory/trips?productId=60cb4b03ac1aaf0da4ebeb0b&originId'
            '=60f8a92b3efac905d82d34b0&destinationId=619bddd4bff5aa06bad42472&departureDate={'
            '}&fareIds=60d0a7e3767d7c05d280bcd7%3A1&channel=websales&showSoldOutTrips=true&providerId'
            '=60cb4b03ac1aaf0da4ebeb0a&isChange=false&currency=CAD&x-api-key=2d9333f4-1f35-4fc2-b6e3-9f9b6d5499ba'
            ''.format(date))

        onexJson = onexBus.json()

        bbbb = onexJson['trips']['departures']
        for x in bbbb:

            departureTime = x['departure']
            arrivalTime = x['arrival']
            stock = x['manifestAvailability']['available']

            for i in x['fareClasses'][0]['fares']:
                priceUno = i['valueToDisplay']

            price = "{:.2f}".format(float(priceUno))

            allBus['OnexBus'].append({"departureTime": departureTime, "arrivalTime": arrivalTime, "Price": price,
                                      "stockLevels": stock})

        #Flix Bus

        aa = requests.get(
            'https://global.api.flixbus.com/search/service/v4/search?from_city_id=347f9e9d-0c48-4770-90f6-cc6a18802bfa&to_city_id=41d79c93-0374-47f3-8f3a-bd154f55153a&departure_date={}.{}.{}&products=%7B%22adult%22%3A1%7D&currency=CAD&locale=en_CA&search_by=cities&include_after_midnight_rides=1'.format(day, month, year))
        bb = aa.json()
        x = bb['trips'][0]['results']
        for i in x:
            allThis = x[i]

            available = allThis['available']['seats']
            if int(available) > 0:
                departure = allThis['departure']['date']
                departureTime = getTime(departure)
                arrival = allThis['arrival']['date']
                arrivalTime = getTime(arrival)

                price = allThis['price']['total']

                stock = available


                allBus['FlixBus'].append({"departureTime": departureTime, "arrivalTime": arrivalTime, "Price": price,
                                          "stockLevels": stock})


        return allBus

def user():
    askUser = input('Do You Want To See Bus Times? (y/n): ').lower()

    today = datetime.now()

    setDate = True
    while setDate:
        whatDate = input('For What Day Would You Like To Check Bus Times (EG. 27): ')

        if int(whatDate) > 0 and int(whatDate) <= 31:
            if int(whatDate) > int(today.day):
                whatDate = '2022-{}-{}'.format(today.month, whatDate)
                setDate = False
            else:
                print('Date Has Already Passed, Try Again \n')

        else:
            print('Invalid Day, Try Again\n')


    if askUser == 'y':
        print('')
        print('Grabbing all available bus routes...\n\n')

        allBus = getBus(whatDate)
        print('ALL AVAILABLE BUSSES FOR: {}'.format(whatDate))
        with open('busOutput.txt', 'w') as f:
            f.write(('ALL AVAILABLE BUSSES FOR: {} \n\n'.format(whatDate)))
            for x in allBus:
                print(' ')
                print('Bus Company: {}\n'.format(x))
                f.write('Bus Company: {}\n\n'.format(x))
                counter = 1
                for i in allBus[x]:
                    print('{} Option {}: '.format(x, counter))
                    f.write(('{} Option {}: \n'.format(x, counter)))
                    for j in i:
                        print('{}: {}'.format(j, i[j]))
                        f.write('{}: {}\n'.format(j, i[j]))

                    counter += 1
                    print(' - - - - - - - - - -')
                    f.write(' - - - - - - - - - -\n')
                print('\n')
                f.write('\n')

        userNice = input('Would You like to see that information a little better formatted (y/n): ').lower()
        if userNice == 'y':
            printNicely(whatDate, allBus)

        else:
            print('Ok Goodbye!')



    else:
        print('Goodbye')
        return

user()
