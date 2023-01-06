# AGSO water meter API client

The municipality Knokke-Heist at the coast of Belgium has it's own drinking
water company which is called AGSO (Autonome Gemeentelijk
StadsOntwikkelingsbedrijf), which loosely translates to 'Autonomous city
development company'. Recently they started rolling out smart water meters. In
my home it is the 'Kamstrup MULTICAL® 21' meter which is Sigfox connected.

The company has a website on which you can login to see your daily
consumption and other data such as temperature, flow rate, ... This repository
contains a Python client library for the API behind this website. This library 
was created to support the accompanying Home Assistant integration.