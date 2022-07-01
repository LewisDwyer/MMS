from locale import currency


def nextSmallest(arr, x):
    try:
        top = len(arr) -1
        curr = 0
        bot = 0
        
        # fail fast if x is less than the smallest value
        if x < arr[0]:
            return -1

        # ghetto binary search
        while bot <= top:
            curr = (top + bot) // 2

            # top half
            if (x > arr[curr]):
                bot = curr + 1

            # bottom half
            elif(x < arr[curr]):
                top = curr - 1

            # equal
            else:
                return arr[curr]

        # should be next smallest..
        return arr[top]
    except:
        return -1

