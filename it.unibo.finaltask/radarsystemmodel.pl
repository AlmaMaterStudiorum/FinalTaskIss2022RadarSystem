%====================================================================================
% radarsystemmodel description   
%====================================================================================
mqttBroker("broker.hivemq.com", "1883", "unibo/marchesini/sonar/events").
context(ctxpc, "localhost",  "TCP", "10000").
 qactor( controller, ctxpc, "it.unibo.controller.Controller").
  qactor( sonar, ctxpc, "it.unibo.sonar.Sonar").
  qactor( radar, ctxpc, "it.unibo.radar.Radar").
