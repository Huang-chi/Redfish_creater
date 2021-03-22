Redfish_creater
=========================================================

### Architecture:
*	Adoption: Binary tree
*	Node :  RedfishNode
	*	Architecture:
	    *	key: The key represents as the path.
		    - Ex: /redfish/v1/Systems
		    
	    *	data: The data represents as the redfish schema.
		    - Ex. {Id: xxx, Name: yyy}
	    *	type: The type represents as the resource name.
		    - Ex. ComputeSystemCollection
	    *	head: The link connects last node.
	    *	tail: The link connects next node on different level.
	    *	right: The link connects next node on same level.

----------------------------------------------------------

### ***Right now:***

Redfish_data 	->	None
		|
Systems			<->	437XR1138R2
		|
Chassis 		<->	1U
		|
Managers		<->	BMC
		|
TaskService		->	None
		|
SessionService	->	None
		|
AccountService	->	None
		|
EventService	->	None
		|
Subscriptions	->	None

----------------------------------------------------------
### CLI design:

*	Search the info of special node
*	Command:
	*	Redfish >> show(Show)    
	     - Show info for all node (_key, data, root, type, head, tail, right)
	*	Redfish >> configure
	*	Redfish (configure) >> redfish_data/Systems/index.json
 
*	generater design:
	*	‘-U’,  ‘--uri’ : Enter the special domain
	*	‘-R’,  ’--resource’ : Install the reference resource
	*	‘-O’ : Open the debug mode
 

