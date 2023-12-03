// ignore_for_file: file_names

import 'process.dart';

class StartPackage{
  String cpuAlgorithm;
  String memoryAlgorithm;
  int quantum;
  int overHead;
  double delay;
  
  List <Process> process;

  StartPackage({
    required this.cpuAlgorithm,
    required this.memoryAlgorithm,
    required this.quantum,
    required this.overHead,
    required this.delay,
    required this.process
  });

  Map toJson(){
    List<Map> process= this.process.map((i) => i.toJson()).toList();
    return {
      'cpuAlgorithm': cpuAlgorithm,
      'memoryAlgorithm': memoryAlgorithm,
      'quantum': quantum,
      'overHead': overHead,
      'delay': delay,
      'process': process
    };
  }
}