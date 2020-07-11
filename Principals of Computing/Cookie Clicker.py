"""
Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_produced = 0.0
        self._cookies_in_hand = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("Total cookies produced is: " + str(self._total_cookies_produced) + 
                "\nCookies in hand is: " + str(self._cookies_in_hand) + "\nCurrent time is: " 
                + str(self._current_time) + "\nCurrent CPS is: " + str(self._current_cps))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies_in_hand
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        returnvalue = list()
        returnvalue.extend(self._history)
        return returnvalue

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if(cookies <= self._cookies_in_hand or self._current_cps == 0.0):
            return 0.0
        return math.ceil((cookies - self._cookies_in_hand) / (self._current_cps))
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if(time > 0.0):
            self._current_time += time
            self._cookies_in_hand += self._current_cps * time
            self._total_cookies_produced += self._current_cps * time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if(self._cookies_in_hand < cost):
            return None
        self._cookies_in_hand -= cost
        self._current_cps += additional_cps
        (self._history).append((self._current_time, item_name, cost, self._total_cookies_produced))

        
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clicker = ClickerState()
    build_info = build_info.clone()
    while clicker.get_time() <= duration:
        next_item = strategy(clicker.get_cookies(), clicker.get_cps(), 
                    clicker.get_history(), duration - clicker.get_time(), build_info)
        if(next_item == None):
            clicker.wait(duration - clicker.get_time())
            return clicker
        cost_of_item = build_info.get_cost(next_item)
        time_until_next_item = clicker.time_until(cost_of_item)
        if(time_until_next_item + clicker.get_time() > duration):
            clicker.wait(duration - clicker.get_time())
            return clicker
        clicker.wait(time_until_next_item)
        clicker.buy_item(next_item, cost_of_item, build_info.get_cps(next_item))
        build_info.update_item(next_item)
    return clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies_in_time_left = cookies + cps * time_left
    all_items = build_info.build_items()
    price_of_cheapest_item = build_info.get_cost(all_items[0])
    cheapest_item = all_items[0]
    for item in all_items:
        if(build_info.get_cost(item) < price_of_cheapest_item):
            cheapest_item = item
            price_of_cheapest_item = build_info.get_cost(item)
    if(cookies_in_time_left >= price_of_cheapest_item):
        return cheapest_item
    return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies_in_time_left = cookies + cps * time_left
    all_items = build_info.build_items()
    price_of_next_item = 0
    next_item = None
    for item in all_items:
        if(cookies_in_time_left >= build_info.get_cost(item) > price_of_next_item):
            next_item = item
            price_of_next_item = build_info.get_cost(item)
    return next_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cookies_in_time_left = cookies + cps * time_left
    all_items = build_info.build_items()
    best_cps_per_dollar = 0.0
    next_item = None
    for item in all_items:
        if(cookies_in_time_left / 2  >= build_info.get_cost(item) 
           and (build_info.get_cps(item) / build_info.get_cost(item) > best_cps_per_dollar)):
            best_cps_per_dollar = build_info.get_cps(item) / build_info.get_cost(item)
            next_item = item
    return next_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
    

