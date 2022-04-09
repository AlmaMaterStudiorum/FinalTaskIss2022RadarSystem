/* Generated by AN DISI Unibo */ 
package it.unibo.controller

import it.unibo.kactor.*
import alice.tuprolog.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
	
class Controller ( name: String, scope: CoroutineScope  ) : ActorBasicFsm( name, scope ){

	override fun getInitialState() : String{
		return "initState"
	}
	@kotlinx.coroutines.ObsoleteCoroutinesApi
	@kotlinx.coroutines.ExperimentalCoroutinesApi			
	override fun getBody() : (ActorBasicFsm.() -> Unit){
		return { //this:ActionBasciFsm
				state("initState") { //this:State
					action { //it:State
						println("Enter initState")
					}
					 transition( edgeName="goto",targetState="wait", cond=doswitch() )
				}	 
				state("wait") { //this:State
					action { //it:State
						println("$name in ${currentState.stateName} | $currentMsg")
						stateTimer = TimerActor("timer_wait", 
							scope, context!!, "local_tout_controller_wait", 1000.toLong() )
					}
					 transition(edgeName="t00",targetState="timeout",cond=whenTimeout("local_tout_controller_wait"))   
				}	 
				state("timeout") { //this:State
					action { //it:State
						println("$name in ${currentState.stateName} | $currentMsg")
						request("coordrequest", "coordrequest(X)" ,"sonar" )  
					}
					 transition( edgeName="goto",targetState="waitforresponse", cond=doswitch() )
				}	 
				state("waitforresponse") { //this:State
					action { //it:State
						println("$name in ${currentState.stateName} | $currentMsg")
					}
					 transition(edgeName="t01",targetState="handlesonarresponse",cond=whenReply("coordresponse"))
				}	 
				state("handlesonarresponse") { //this:State
					action { //it:State
						println("$name in ${currentState.stateName} | $currentMsg")
						println("controller receives answer")
						if( checkMsgContent( Term.createTerm("coordresponse(X)"), Term.createTerm("coordresponse(X)"), 
						                        currentMsg.msgContent()) ) { //set msgArgList
								println("coordresponse:coordresponse(DIST)")
								 var Dist = payloadArg(0).toInt()    
								forward("updateradar", "updateradar($Dist)" ,"radar" ) 
						}
					}
					 transition( edgeName="goto",targetState="wait", cond=doswitch() )
				}	 
			}
		}
}