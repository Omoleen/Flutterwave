from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class TransactionView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            if 0 < len(request.data.get('SplitInfo')) <= 20:
                request.data['Balance'] = request.data.get('Amount')
                flat = [i for i in request.data.get('SplitInfo') if i.get('SplitType') == 'FLAT']
                percentage = [i for i in request.data.get('SplitInfo') if i.get('SplitType') == 'PERCENTAGE']
                ratio = [i for i in request.data.get('SplitInfo') if i.get('SplitType') == 'RATIO']
                initbalance = request.data.get('Amount')
                if len(flat) > 0:
                    for i in flat:
                        initbalance -= i.get('SplitValue')
                        i['Amount'] = i.get('SplitValue')
                        i.pop('SplitValue')
                        i.pop('SplitType')
                        # print(i['Amount'])
                        if i['Amount'] > request.data.get('Amount'):
                            custom = {'message': f'Split Amount for {i.get("SplitEntityId")} greater than Transaction Amount'}
                            return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                        elif i['Amount'] < 0:
                            custom = {'message': f'Split Amount for {i.get("SplitEntityId")} is lesser than Zero'}
                            return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                        # print(f'{initbalance}')
                if len(percentage) > 0:
                    for i in percentage:
                        i['Amount'] = i.get('SplitValue')/100 * initbalance
                        initbalance -= i.get('Amount')
                        i.pop('SplitValue')
                        i.pop('SplitType')
                        # print(i['Amount'])
                        if i['Amount'] > request.data.get('Amount'):
                            custom = {'message': f'Split Amount for {i.get("SplitEntityId")} greater than Transaction Amount'}
                            return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                        elif i['Amount'] < 0:
                            custom = {'message': f'Split Amount for {i.get("SplitEntityId")} is lesser than Zero'}
                            return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                        # print(f'{initbalance}')
                if len(ratio) > 0:
                    ratiobal = initbalance
                    sumtotal = sum([a.get('SplitValue') for a in ratio])
                    for i in ratio:
                        i['Amount'] = i.get('SplitValue')/sumtotal * ratiobal
                        initbalance -= i.get('Amount')
                        i.pop('SplitValue')
                        i.pop('SplitType')
                        # print(i['Amount'])
                        if i['Amount'] > request.data.get('Amount'):
                            custom = {'message': f'Split Amount for {i.get("SplitEntityId")} greater than Transaction Amount'}
                            return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                        elif i['Amount'] < 0:
                            custom = {'message': f'Split Amount for {i.get("SplitEntityId")} is lesser than Zero'}
                            return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                        # print(f'{initbalance}')
                request.data['Balance'] = initbalance
                if request.data['Balance'] < 0:
                    custom = {'message': 'Split sum greater than Transaction Amount'}
                    return Response(custom, status=status.HTTP_400_BAD_REQUEST)
                custom = {
                    "ID": request.data.get("ID"),
                    "Balance": request.data.get("Balance"),
                    "SplitBreakdown": [*flat, *percentage, *ratio]
                }
                return Response(custom, status=status.HTTP_201_CREATED)
            elif len(request.data.get('SplitInfo')) > 20:
                custom = {'message': 'Maximum of 20 entries'}
                return Response(custom, status=status.HTTP_400_BAD_REQUEST)
            else:
                custom = {'message': 'Minimum of 1 entry'}
                return Response(custom, status=status.HTTP_400_BAD_REQUEST)
        except:
            custom = {'message': 'Invalid Input'}
            return Response(custom, status=status.HTTP_400_BAD_REQUEST)