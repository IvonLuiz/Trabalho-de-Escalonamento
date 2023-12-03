// ignore_for_file: library_prefixes

import 'dart:convert';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'process.dart';
import 'startPackage.dart';
import 'dart:math';

void main() {
  runApp(const EscalonadorWeb());
}

class EscalonadorWeb extends StatelessWidget {
  const EscalonadorWeb({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Escalonador SO',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.purple),
        useMaterial3: true,
      ),
      home: const HomeScreen(
        title: 'MATA58 UFBA 2023.2 | Escalonador de Processos - Guilherme Caria, Camila Almeida, Felipe Freire e Ivon Luiz'
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;
  
  @override
  State<HomeScreen> createState(){
    return HomeScreenState();
  }
}

class HomeScreenState extends State<HomeScreen> {
  String activeButtonProcess= 'fifo'; //1= FIFO, 2=EDF, 3= RR, 4=SJF
  String activeButtonMemory= 'fifo'; //1= FIFO, 2= LRU
  double delayValue= 0.5;
  var buttonColorsProcess= [Colors.purple, Colors.white, Colors.white, Colors.white];
  var textColorProcess= [
    const Color.fromRGBO(255, 255, 255, 1),
    const Color.fromRGBO(156, 39, 176, 1),
    const Color.fromRGBO(156, 39, 176, 1),
    const Color.fromRGBO(156, 39, 176, 1)
  ];
  var buttonColorsMemory= [Colors.purple, Colors.white];
  var textColorMemory= [
    const Color.fromRGBO(255, 255, 255, 1),
    const Color.fromRGBO(156, 39, 176, 1)
  ];

  TextEditingController quantumValue= TextEditingController();
  TextEditingController overheadValue= TextEditingController();
  TextEditingController execTimeValue= TextEditingController();
  TextEditingController pagesValue= TextEditingController();
  TextEditingController deadlineValue= TextEditingController();
  TextEditingController arrivalValue= TextEditingController();

  //Lista de processos
  List<Process> process= List.empty(growable: true);
  int processId= 1;

  //Cores dos processos
  Random random= Random();
  List<Color> processColors= List.empty(growable: true);

  //Valor do switch (True= mostrar id, false= mostrar cores)
  bool switchValue= false;

  //String JSON de configuração inicial
  late String startConfig;

// webSocket para comunicação com Backend
  late IO.Socket socket;

// Valor do disco atual
  List<int> disk= List.filled(250, 0); //Valor Inicial

// Valor da RAM atual
  List<int> ram= List.filled(50, 0); //Valor Inicial

//Lista de TableRows para o disk
  List<TableRow> diskTableRows= [];

//Lista de TableRows para a ram
  List<TableRow> ramTableRows= [];

//Espaço livre no disco
  int diskSpace= 250;

//Tamanho da RAM
  final ramSize= 50;

//Mensagem de erro
  String errorProcessCreation= '';

//ResetState 0= nenhumReset, 1= Primeiro clique, 2= Segundo Clique
  int resetState= 0;

//Texto do botão de reset
  String resetButtonText= 'Reset Algorithm';

//Cor do botão de reset
  Color resetButtonColor= Colors.orange;

//Cor da borda da mensagem de erro
  Color errorBorderColor= Colors.transparent;

//Gantt Matrix

  List<List<int>> gantt= [];

//Cores de Gantt
  List<Color> ganttColors= [
    Colors.grey, //Não chegou ou finalizou
    Colors.yellow, //Aguardando execução
    Colors.green, //Executando
    Colors.red, //Troca de contexto(overhead)
    Colors.black  //Estouro de deadline
  ];


//Variáveis para navegar na matriz de Gantt
  int ganttColumn= 0;
  int ganttRow= 0;

//Horizontal Scroll controller
  ScrollController con= ScrollController();
  ScrollController ganttCon= ScrollController();

//Variável para guardar o turnaround
  double turnaround= 0;


  @override
  void initState() {
    initSocket();
    diskTableRows= getRow(disk, 25);
    ramTableRows= getRow(ram, 10);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Scrollbar(
            thumbVisibility: true,
            scrollbarOrientation: ScrollbarOrientation.bottom,
            controller: con,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              controller: con,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[

                  const SizedBox(height: 40,),

                  Row(
                    
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[

                      const SizedBox(width: 50),

                      //Botões do escalonador de processos
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          const Text(
                            'Método de escalonamento',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 20,
                            ),
                          ),

                          const SizedBox(height: 10,),

                          //Botões de cima para escalonador
                          Wrap(
                            spacing: 20,
                            children: <Widget>[
                              //Botão FIFO
                              OutlinedButton(
                                      style: OutlinedButton.styleFrom(
                                        minimumSize: const Size(200, 40),
                                        foregroundColor: Colors.purple,
                                        backgroundColor: buttonColorsProcess[0],
                                        side: const BorderSide(
                                          color: Colors.purple,
                                          width: 2
                                        ),
                                      ),
                                      onPressed:(){
                                        setState(() {
                                          activeButtonProcess= 'fifo';
                                          buttonColorsProcess[0]= Colors.purple;
                                          buttonColorsProcess[1]= Colors.white;
                                          buttonColorsProcess[2]= Colors.white;
                                          buttonColorsProcess[3]= Colors.white;
                                          textColorProcess[0]= const Color.fromRGBO(255, 255, 255, 1);
                                          textColorProcess[1]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[2]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[3]= const Color.fromRGBO(156, 39, 176, 1);
                                        });
                                      },
                                      child: Text(
                                        'First In First Out',
                                        style: TextStyle(
                                          color: textColorProcess[0],
                                        ),
                                      ),
                                    ),

                              //Botão EDF
                              OutlinedButton(
                                      style: OutlinedButton.styleFrom(
                                        minimumSize: const Size(200, 40),
                                        foregroundColor: Colors.purple,
                                        backgroundColor: buttonColorsProcess[1],
                                        side: const BorderSide(
                                          color: Colors.purple,
                                          width: 2
                                        ),
                                      ),
                                      onPressed:(){
                                        setState(() {
                                          activeButtonProcess= 'edf';
                                          buttonColorsProcess[0]= Colors.white;
                                          buttonColorsProcess[1]= Colors.purple;
                                          buttonColorsProcess[2]= Colors.white;
                                          buttonColorsProcess[3]= Colors.white;
                                          textColorProcess[0]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[1]= const Color.fromRGBO(255, 255, 255, 1);
                                          textColorProcess[2]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[3]= const Color.fromRGBO(156, 39, 176, 1);
                                        });
                                      },
                                      child: Text(
                                        'Earliest Deadline First',
                                        style: TextStyle(
                                          color: textColorProcess[1],
                                        ),
                                      ),
                                    ),
                            ],
                          ),

                          const SizedBox(height: 20,), //Espaço entre Rows

                          //Botões de baixo para o escalonador
                          Wrap(
                            spacing: 20,
                            children: <Widget>[

                              //Botão Round Robin
                              OutlinedButton(
                                      style: OutlinedButton.styleFrom(
                                        minimumSize: const Size(200, 40),
                                        foregroundColor: Colors.purple,
                                        backgroundColor: buttonColorsProcess[2],
                                        side: const BorderSide(
                                          color: Colors.purple,
                                          width: 2
                                        ),
                                      ),
                                      onPressed:(){
                                        setState(() {
                                          activeButtonProcess= 'rr';
                                          buttonColorsProcess[0]= Colors.white;
                                          buttonColorsProcess[1]= Colors.white;
                                          buttonColorsProcess[2]= Colors.purple;
                                          buttonColorsProcess[3]= Colors.white;
                                          textColorProcess[0]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[1]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[2]= const Color.fromRGBO(255, 255, 255, 1);
                                          textColorProcess[3]= const Color.fromRGBO(156, 39, 176, 1);
                                        });
                                      },
                                      child: Text(
                                        'Round Robin',
                                        style: TextStyle(
                                          color: textColorProcess[2],
                                        ),
                                      ),
                                    ),

                              //Botão Shortest Job First
                              OutlinedButton(
                                      style: OutlinedButton.styleFrom(
                                        minimumSize: const Size(200, 40),
                                        foregroundColor: Colors.purple,
                                        backgroundColor: buttonColorsProcess[3],
                                        side: const BorderSide(
                                          color: Colors.purple,
                                          width: 2
                                        ),
                                      ),
                                      onPressed:(){
                                        setState(() {
                                          activeButtonProcess= 'sjf';
                                          buttonColorsProcess[0]= Colors.white;
                                          buttonColorsProcess[1]= Colors.white;
                                          buttonColorsProcess[2]= Colors.white;
                                          buttonColorsProcess[3]= Colors.purple;
                                          textColorProcess[0]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[1]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[2]= const Color.fromRGBO(156, 39, 176, 1);
                                          textColorProcess[3]= const Color.fromRGBO(255, 255, 255, 1);
                                        });
                                      },
                                      child: Text(
                                        'Shortest Job First',
                                        style: TextStyle(
                                          color: textColorProcess[3],
                                        ),
                                      ),
                                    ),
                            ],
                          ),

                          const SizedBox(height: 40,),

                          //Botões da MMU
                          Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.start,
                            children: <Widget>[
                              const Text(
                                'Método de Paginação',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 20,
                                ),
                              ),
                              

                              const SizedBox(height: 10,),

                              //Botões de cima para escalonador
                              Wrap(
                                spacing: 20,
                                children: <Widget>[
                                  //Botão FIFO
                                  OutlinedButton(
                                          style: OutlinedButton.styleFrom(
                                            minimumSize: const Size(200, 40),
                                            foregroundColor: Colors.purple,
                                            backgroundColor: buttonColorsMemory[0],
                                            side: const BorderSide(
                                              color: Colors.purple,
                                              width: 2
                                            ),
                                          ),
                                          onPressed:(){
                                            setState(() {
                                              activeButtonMemory= 'fifo';
                                              buttonColorsMemory[0]= Colors.purple;
                                              buttonColorsMemory[1]= Colors.white;
                                              textColorMemory[0]= const Color.fromRGBO(255, 255, 255, 1);
                                              textColorMemory[1]= const Color.fromRGBO(156, 39, 176, 1);
                                            });
                                          },
                                          child: Text(
                                            'First in First Out',
                                            style: TextStyle(
                                              color: textColorMemory[0],
                                            ),
                                          ),
                                        ),

                                  //Botão LRU
                                  OutlinedButton(
                                          style: OutlinedButton.styleFrom(
                                            minimumSize: const Size(200, 40),
                                            foregroundColor: Colors.purple,
                                            backgroundColor: buttonColorsMemory[1],
                                            side: const BorderSide(
                                              color: Colors.purple,
                                              width: 2
                                            ),
                                          ),
                                          onPressed:(){
                                            setState(() {
                                              activeButtonMemory= 'lru';
                                              buttonColorsMemory[0]= Colors.white;
                                              buttonColorsMemory[1]= Colors.purple;
                                              textColorMemory[0]= const Color.fromRGBO(156, 39, 176, 1);
                                              textColorMemory[1]= const Color.fromRGBO(255, 255, 255, 1);

                                            });
                                          },
                                          child: Text(
                                            'Least Recently Used',
                                            style: TextStyle(
                                              color: textColorMemory[1],
                                            ),
                                          ),
                                        ),
                                ],
                              ),

                            ],
                          ),

                          const SizedBox(height: 40,),

                          //Configurações do quantum, Overhead e Delay
                          Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: <Widget>[
                              const Text(
                                'Configurações Adicionais',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 20,
                                ),
                              ),

                            //Quantum
                            SizedBox(
                              width: 150,
                              child: TextField(
                                controller: quantumValue,
                                decoration: const InputDecoration(
                                  label: Text(
                                    'Quantum',
                                    style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      color: Colors.purple,
                                      fontSize: 16,
                                    ),
                                  )
                                ),
                                keyboardType: TextInputType.number,
                                inputFormatters: <TextInputFormatter>[
                                  FilteringTextInputFormatter.digitsOnly
                                ],
                              ),
                            ),

                            //Overhead
                            SizedBox(
                              width: 150,
                              child: TextField(
                                controller: overheadValue,
                                decoration: const InputDecoration(
                                  label: Text(
                                    'Overhead',
                                    style: TextStyle(
                                      fontWeight: FontWeight.bold,
                                      color: Colors.purple,
                                      fontSize: 16,
                                    ),
                                  )
                                ),
                                keyboardType: TextInputType.number,
                                inputFormatters: <TextInputFormatter>[
                                  FilteringTextInputFormatter.digitsOnly
                                ],
                              ),
                            ),

                            const SizedBox(height: 20,),

                            const Text(
                              'Delay de execução',
                              style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.purple,
                              fontSize: 16,
                              )
                            ),
                            //Slider para o delay
                            Slider(
                              min: 0.1,
                              max: 2,
                              value: delayValue, 
                              onChanged: (value){
                                setState(() {
                                  delayValue= double.parse(value.toStringAsFixed(3));
                                });
                              }
                            ),
                            Text(
                              'Delay de $delayValue segundos',
                              style: const TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                              fontSize: 16,
                              )
                            ),

                            ],
                          ),

                          //Visualização da memória
                          const SizedBox(height: 40,),

                          Wrap(
                            alignment: WrapAlignment.center,
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              const Text(
                                'Visualizar memórias por PID',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 20,
                                ),
                              ),

                              const SizedBox(width: 20,),

                              
                              Switch(
                                value: switchValue, 
                                onChanged: (value){
                                  setState(() {
                                    switchValue= value;
                                    diskTableRows= getRow(disk, 25);
                                    ramTableRows= getRow(ram, 10);
                                  });
                                }
                              ),
                            ],
                          ),



                        ],
                      ),

                      const SizedBox(width: 50,),



                      //Editor de processos
                      Wrap(
                        alignment: WrapAlignment.start,
                        children: <Widget>[
                          Container(
                            height: 600,
                            width: 500,
                            decoration: const BoxDecoration(
                              borderRadius: BorderRadius.all(Radius.circular(40)),
                              color: Colors.purple
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: <Widget>[

                                const SizedBox(height: 20,),

                                const Text(
                                  'Editor de processos',
                                  style: TextStyle(
                                    fontSize: 30,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),

                                const SizedBox(height: 10),

                                //Mensagem de erro
                                Container(
                                  alignment: Alignment.center,
                                  height: 30,
                                  width: 320,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.all(Radius.circular(40)),
                                    color: errorBorderColor,
                                  ),
                                  child:Text(
                                  errorProcessCreation,
                                    style: const TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.purple
                                    ),
                                  ),
                                ),

                                const SizedBox(height: 10),

                                Wrap(
                                  spacing: 20,
                                  children: <Widget>[


                                    //Tempo de execução
                                    SizedBox(
                                      width: 200,
                                      child: TextField(
                                        controller: execTimeValue,
                                        cursorColor: Colors.white,
                                        style: const TextStyle(color: Colors.white),
                                        decoration: const InputDecoration(
                                          enabledBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          focusedBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          label: Text(
                                            'Tempo de Execução',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.white,
                                              fontSize: 16,
                                            ),
                                          )
                                        ),
                                        keyboardType: TextInputType.number,
                                        inputFormatters: <TextInputFormatter>[
                                          FilteringTextInputFormatter.digitsOnly
                                        ],
                                      ),
                                    ),

                                    //Número de páginas
                                    SizedBox(
                                      width: 200,
                                      child: TextField(
                                        controller: pagesValue,
                                        cursorColor: Colors.white,
                                        style: const TextStyle(color: Colors.white),
                                        decoration: const InputDecoration(
                                          enabledBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          focusedBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          label: Text(
                                            'Páginas',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.white,
                                              fontSize: 16,
                                            ),
                                          )
                                        ),
                                        keyboardType: TextInputType.number,
                                        inputFormatters: <TextInputFormatter>[
                                          FilteringTextInputFormatter.digitsOnly
                                        ],
                                      ),
                                    ),


                                  ],
                                ),

                                const SizedBox(height: 10,),
                          
                                Wrap(
                                  spacing: 20,
                                  children: <Widget>[

                                    //Deadline
                                    SizedBox(
                                      width: 200,
                                      child: TextField(
                                        controller: deadlineValue,
                                        cursorColor: Colors.white,
                                        style: const TextStyle(color: Colors.white),
                                        decoration: const InputDecoration(
                                          enabledBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          focusedBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          label: Text(
                                            'Deadline',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.white,
                                              fontSize: 16,
                                            ),
                                          )
                                        ),
                                        keyboardType: TextInputType.number,
                                        inputFormatters: <TextInputFormatter>[
                                          FilteringTextInputFormatter.digitsOnly
                                        ],
                                      ),
                                    ),

                                    //Momento de chegada
                                    SizedBox(
                                      width: 200,
                                      child: TextField(
                                        controller: arrivalValue,
                                        cursorColor: Colors.white,
                                        style: const TextStyle(color: Colors.white),
                                        decoration: const InputDecoration(
                                          enabledBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          focusedBorder: UnderlineInputBorder(
                                            borderSide: BorderSide(color: Colors.white)
                                          ),
                                          label: Text(
                                            'Chegada',
                                            style: TextStyle(
                                              fontWeight: FontWeight.bold,
                                              color: Colors.white,
                                              fontSize: 16,
                                            ),
                                          )
                                        ),
                                        keyboardType: TextInputType.number,
                                        inputFormatters: <TextInputFormatter>[
                                          FilteringTextInputFormatter.digitsOnly
                                        ],
                                      ),
                                    ),


                                  ],
                                ),

                                const SizedBox(height: 10,),


                                //Botão para criar o processo
                                
                                OutlinedButton(
                                  style: OutlinedButton.styleFrom(
                                    minimumSize: const Size(450, 50),
                                    foregroundColor: Colors.white,
                                    side: const BorderSide(
                                      color: Colors.white,
                                      width: 3
                                    ),
                                  ),
                                  onPressed:(){
                                    String execTime= execTimeValue.text.trim();
                                    String pages= pagesValue.text.trim();
                                    String deadline= deadlineValue.text.trim();
                                    String arrivalTime= arrivalValue.text.trim();
                                    if(execTime.isNotEmpty && pages.isNotEmpty && deadline.isNotEmpty && arrivalTime.isNotEmpty){
                                    
                                      setState((){

                                        //Processo não cabe no disco nem na ram
                                        if(diskSpace - int.parse(pages) < 0 && int.parse(pages)>ramSize){
                                          errorProcessCreation= 'Espaço insuficiente na RAM e no Disco!';
                                          errorBorderColor= Colors.white;
                                        }
                                        //Processo não cabe no disco nem na ram
                                        else if(diskSpace - int.parse(pages) < 0){
                                          errorProcessCreation= 'Espaço insuficiente no Disco!';
                                          errorBorderColor= Colors.white;
                                        }
                                        //Processo não cabe no disco nem na ram
                                        else if(int.parse(pages)>ramSize){
                                          errorProcessCreation= 'Espaço insuficiente na RAM!';
                                          errorBorderColor= Colors.white;
                                        }

                                        //Criamos o processo e colocamos na lista
                                        else{
                                          errorBorderColor= Colors.transparent;
                                          diskSpace-= int.parse(pages);
                                          errorProcessCreation= '';
                                          process.add(
                                            Process(
                                              id: processId, 
                                              arrivalTime: int.parse(arrivalTime), 
                                              execTime: int.parse(execTime), 
                                              deadline: int.parse(deadline), 
                                              numberOfPages: int.parse(pages)));

                                            processId++;

                                            execTimeValue.text= '';
                                            pagesValue.text= '';
                                            deadlineValue.text= '';
                                            arrivalValue.text= '';

                                          processColors.add(Color.fromRGBO(
                                            random.nextInt(255),
                                            random.nextInt(255),
                                            random.nextInt(255),
                                            1
                                          ));
                                        }
                                      });
                                    }
                                  },

                                  
                                  child: const Text(
                                    'Criar Processo',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 20,
                                    ),
                                  ),
                                ),

                                const SizedBox(height: 30,),

                              ],
                            ),
                          ),

                          const SizedBox(width: 30,),

                          //Lista de processos criados
                          SizedBox(
                            width: 520,
                            height: 600,
                            child:ListView.builder(
                                itemCount: process.length,
                                itemBuilder: (context,index) => getTile(index, process, processColors),
                              )
                          ),

        
                        ],
                      ),




                  ],
                  ),

                  const SizedBox(height: 60,),


                  Wrap(
                    children: <Widget>[

                      //Legenda do gráfico de Gantt
                      Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                                'Legenda',
                                style: TextStyle(
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold
                                ),
                              ),

                              const SizedBox(height: 10),

                          Wrap(
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              
                              Padding(
                                padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
                                child: Container(
                                  alignment: Alignment.center,
                                  height: 20,
                                  width: 20,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.all(Radius.circular(8)),
                                    color: ganttColors[0],
                                  ),
                                ),
                              ),

                              const SizedBox(width: 5),

                              const Text(
                                'Não chegou / Finalizou',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold
                                ),
                              ),
                            ],

                          ),

                          const SizedBox(height: 5),
                          
                          Wrap(
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              
                              Padding(
                                padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
                                child: Container(
                                  alignment: Alignment.center,
                                  height: 20,
                                  width: 20,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.all(Radius.circular(8)),
                                    color: ganttColors[1],
                                  ),
                                ),
                              ),

                              const SizedBox(width: 5),

                              const Text(
                                'Aguardando Execução',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold
                                ),
                              ),
                            ],

                          ),
                          
                          const SizedBox(height: 5),
                          
                          Wrap(
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              
                              Padding(
                                padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
                                child: Container(
                                  alignment: Alignment.center,
                                  height: 20,
                                  width: 20,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.all(Radius.circular(8)),
                                    color: ganttColors[2],
                                  ),
                                ),
                              ),

                              const SizedBox(width: 5),

                              const Text(
                                'Executando',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold
                                ),
                              ),
                            ],

                          ),
                          
                          const SizedBox(height: 5),
                          
                          Wrap(
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              
                              Padding(
                                padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
                                child: Container(
                                  alignment: Alignment.center,
                                  height: 20,
                                  width: 20,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.all(Radius.circular(8)),
                                    color: ganttColors[3],
                                  ),
                                ),
                              ),

                              const SizedBox(width: 5),

                              const Text(
                                'Troca de Contexto (Overhead)',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold
                                ),
                              ),
                            ],

                          ),
                          
                          const SizedBox(height: 5),
                          
                          Wrap(
                            crossAxisAlignment: WrapCrossAlignment.center,
                            children: [
                              
                              Padding(
                                padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
                                child: Container(
                                  alignment: Alignment.center,
                                  height: 20,
                                  width: 20,
                                  decoration: BoxDecoration(
                                    borderRadius: const BorderRadius.all(Radius.circular(8)),
                                    color: ganttColors[4],
                                  ),
                                ),
                              ),

                              const SizedBox(width: 5),

                              const Text(
                                'Estouro de Deadline',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold
                                ),
                              ),
                            ],

                          ),
                        ],
                      ),

                      const SizedBox(width: 210,),

                      //Botão START
                      OutlinedButton(
                              style: OutlinedButton.styleFrom(
                                minimumSize: const Size(300, 60),
                                foregroundColor: Colors.purple,
                                backgroundColor: Colors.green,
                                side: const BorderSide(
                                  color: Colors.green,
                                  width: 2
                                ),
                              ),
                              onPressed:(){
                                if(process.isNotEmpty && quantumValue.text != '' && overheadValue.text != ''){
                                    //Objeto para enviar ao backend
                                    StartPackage package= StartPackage(
                                      cpuAlgorithm: activeButtonProcess, 
                                      memoryAlgorithm: activeButtonMemory, 
                                      quantum: int.parse(quantumValue.text), 
                                      overHead: int.parse(overheadValue.text), 
                                      delay: delayValue, 
                                      process: process
                                    );
                                    startConfig= jsonEncode(package);
                                    //Envia o JSON com os valores
                                    socket.emit('start', startConfig);
                                    gantt= [];
                                    ganttRow= 0;
                                    ganttColumn=0;
                                    turnaround= 0;
                                }
                                setState(() {
                                  resetButtonText= 'Reset Algorithm';
                                  resetButtonColor= Colors.orange;
                                  resetState= 0;
                                });
                              },
                              child: const Text(
                                'Start',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 30,
                                ),
                              ),
                            ),

                      const SizedBox(width: 30,),

                      //Botão Reset
                      OutlinedButton(
                              style: OutlinedButton.styleFrom(
                                minimumSize: const Size(300, 60),
                                foregroundColor: Colors.purple,
                                backgroundColor: resetButtonColor,
                                side: BorderSide(
                                  color: resetButtonColor,
                                  width: 2
                                ),
                              ),
                              onPressed:(){
                                socket.emit('reset_system');
                                //Reseta todos os valores        
                                setState(() {
                                  if(resetState==0){//Primeiro clique
                                    //Mantém os processos e config de timing
                                    resetUI(false);
                                    resetButtonText= 'Reset All';
                                    resetButtonColor= Colors.red;
                                    resetState++;
                                  }   
                                  else if(resetState==1){//Segundo clique
                                    //Reset geral
                                    resetUI(true);
                                    resetButtonText= 'Reset Algorithm';
                                    resetButtonColor= Colors.orange;
                                    resetState= 0;
                                  }
                                });
                              },
                              child:Text(
                                resetButtonText,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 30,
                                ),
                              ),
                            ),

                            const SizedBox(width: 410,),

                    ],
                  ),


                  //Gráfico de Gantt
                  Text(
                    labelGantt(),
                    style: const TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.bold
                    ),
                  ),

                  const SizedBox(height: 10),

                  Wrap(
                    children: [
                      
                      //Container para ID de processos
                      Container(
                        height: getGraphHeight()+10,
                        width: 40,
                        alignment: Alignment.center,
                        decoration: const BoxDecoration(
                          borderRadius: BorderRadius.all(Radius.circular(40)),
                          color: Colors.transparent,
                        ),
                        //Construção das caixas dos processos
                        child: ListView.builder(
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: process.length,
                          itemBuilder: (context,index) => getContainer(index, process, processColors),
                          ),
                      ),
                      
                      Container(

                        
                        //Altura para acomodar o gráfico de gantt
                        height: getGraphHeight()+40,
                        width: getGraphWidth(),
                        alignment: Alignment.center,
                        decoration: const BoxDecoration(
                          borderRadius: BorderRadius.all(Radius.circular(40)),
                          color: Colors.transparent
                        ),

                        //Visualização da matriz de gantt
                        child: Scrollbar(
                          controller: ganttCon,
                          thumbVisibility: true,
                          trackVisibility: true,
                          child: GridView.count(
                            controller: ganttCon,
                            shrinkWrap: true,
                            scrollDirection: Axis.horizontal,
                            crossAxisCount: calculateGanttItemsRow(),
                            children: gridGenerateChild()
                          ),
                        ),
                      ),
                    ],
                  ),

              
                  const SizedBox(height: 80),

                  //Disco e Ram
                  Wrap(
                    alignment: WrapAlignment.center,
                    spacing: 100,
                    children: <Widget>[
                      //DISCO
                      Column(
                        children: [
                          const Text(
                            'Disco',
                            style: TextStyle(
                            fontSize: 30,
                            fontWeight: FontWeight.bold
                            ),
                          ),

                          const SizedBox(height: 20),

                          Container(
                            //height: 800,
                            width: 1000,
                            alignment: Alignment.center,
                            decoration: const BoxDecoration(
                              borderRadius: BorderRadius.all(Radius.circular(40)),
                              //color: Colors.purple
                            ),
                            child: Table(
                              border: TableBorder.all(color: Colors.black),
                              children: diskTableRows,
                            ),
                          ),
                        ],
                      ),


                      //RAM
                      Column(
                        children: [
                          const Text(
                            'RAM',
                            style: TextStyle(
                            fontSize: 30,
                            fontWeight: FontWeight.bold
                            ),
                          ),

                          const SizedBox(height: 20),

                          Container(
                            //height: 500,
                            width: 400,
                            alignment: Alignment.center,
                            decoration: const BoxDecoration(
                              borderRadius: BorderRadius.all(Radius.circular(40)),
                              //color: Colors.purple
                            ),
                            child: Table(
                              border: TableBorder.all(color: Colors.black),
                              children: ramTableRows,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
              
                  const SizedBox(height: 80),

                ],
              )
            ),


          ),
          
          
            
        ),
      ), 
    );
  }

  void recalculateProcessId(){
    processId= process.length+1;
    for(int i= 0; i<process.length; i++){
      process[i].id= i+1;
    }
  }

  Widget getTile(int index, List<Process> process, List<Color> processColors){
    return Card(
      child: ListTile(
        title: Text('Processo ${process[index].id}'),
        subtitle: Text(
         'Tempo: ${process[index].execTime} | Páginas: ${process[index].numberOfPages} | Deadline: ${process[index].deadline} | Chegada: ${process[index].arrivalTime}'
        ),
        trailing: IconButton(
          onPressed: (){
            setState(() {
              process.removeAt(index);
              processColors.removeAt(index);
              recalculateProcessId();
              socket.emit('reset_system');
              resetUI(false);
            });
          }, 
          icon: const Icon(Icons.delete)
        ),
        leading: Icon(Icons.circle, color: processColors[index]),
        contentPadding: const EdgeInsets.all(10),
      ),
    );
  }

  List<TableRow> getRow(List<int>itemList, int columns){
    List<TableRow> listaTableRow= [];
    // ignore: prefer_const_constructors, prefer_const_literals_to_create_immutables
    TableRow row= TableRow(children: []);
    for(int i= 0; i<itemList.length; i+=columns){
      int iterationEnd= i+columns;
      for(int j= i; j<iterationEnd; j++){
        if(switchValue == false){//Mostrar por Cores
          row.children.add(
            Container(
              alignment: AlignmentDirectional.center,
              margin: const EdgeInsets.all(10),
              child: Icon(Icons.circle, color: findColor(itemList[j])),
            )
          );
        }
        else{//Mostrar por PID
          row.children.add(
            Container(
              alignment: AlignmentDirectional.center,
              margin: const EdgeInsets.all(8),
              child: Text(
                '${itemList[j]}',
                style: TextStyle(
                  fontSize: 19.5,
                  fontWeight: FontWeight.bold,
                  color: findColor(itemList[j])
                ),
              ),
            )
          );
        }
      }
      listaTableRow.add(row);
      // ignore: prefer_const_literals_to_create_immutables, prefer_const_constructors
      row= TableRow(children: []);
    }
    return listaTableRow;
  }

  Color findColor(int idToFind){
    if(idToFind == 0){//Branco 100% transparente (disco livre)
      return const Color.fromARGB(0, 255, 255, 255);
    }
    else{
      if(processColors.length < idToFind){
        return const Color.fromARGB(0, 255, 255, 255);
      }
      else{
        return processColors[idToFind-1];
      }
    }
  }


  initSocket(){
    socket = IO.io('http://127.0.0.1:5000', <String, dynamic>{
    'autoConnect': false,
    'transports': ['websocket'],
    });
    socket.connect();
    socket.onConnect((_){
      print('Connected!');
    });
    socket.onDisconnect((_) => print('Connection Disconnection'));
    socket.onConnectError((err) => print(err));
    socket.onError((err) => print(err));
    socket.on('initialValues', (data){
      setState(() {
        disk= data[0]['disk'].cast<int>();
        diskTableRows= getRow(disk, 25);
        ram= data[1]['ram'].cast<int>();
        ramTableRows= getRow(ram, 10);
      });
    });

    socket.on('updatedValues', (dataUpdate){
      setState(() {
        disk= dataUpdate[0]['disk'].cast<int>();
        diskTableRows= getRow(disk, 25);
        ram= dataUpdate[1]['ram'].cast<int>();
        ramTableRows= getRow(ram, 10);
        gantt= [];
        for(int i= 0; i<process.length; i++){
          var aux= dataUpdate[2]['gantt'];
          List<int> auxCast= aux['${i+1}'].cast<int>();
          gantt.add(auxCast);
        }
      });
    });

    // ignore: empty_statements
    socket.on('average_turnaround', (data){
        setState(() {
          turnaround= double.parse(data.toStringAsFixed(2));
        });
    });
  }

  //Código para alterar a label do gráfico de gantt
  String labelGantt(){
    if(turnaround == 0){
      return 'Gráfico de Gantt';
    }
    else{
      return 'Turnaround: $turnaround';
    }
  }

  //Função de reset de UI, true= reseta tudo, false= mantém os processos criados
  void resetUI(bool resetAll){
    setState(() {
      if(resetAll){
        process= List.empty(growable: true);
        processId= 1;
        processColors= List.empty(growable: true);
        quantumValue.text= '';
        overheadValue.text= '';
        delayValue= 0.5;
        switchValue= false;
      }
      turnaround= 0;
      gantt= [];
      ganttRow= 0;
      ganttColumn=0;
      errorBorderColor= Colors.transparent;
      activeButtonProcess= 'fifo'; //1= FIFO, 2=EDF, 3= RR, 4=SJF
      activeButtonMemory= 'fifo'; //1= FIFO, 2= LRU 
      buttonColorsProcess= [Colors.purple, Colors.white, Colors.white, Colors.white];
      textColorProcess= [
        const Color.fromRGBO(255, 255, 255, 1),
        const Color.fromRGBO(156, 39, 176, 1),
        const Color.fromRGBO(156, 39, 176, 1),
        const Color.fromRGBO(156, 39, 176, 1)
      ];
      buttonColorsMemory= [Colors.purple, Colors.white];
      textColorMemory= [
        const Color.fromRGBO(255, 255, 255, 1),
        const Color.fromRGBO(156, 39, 176, 1)
      ];
      disk= List.filled(250, 0); //Valor Inicial
      ram= List.filled(50, 0); //Valor Inicial
      diskTableRows= getRow(disk, 25);
      ramTableRows= getRow(ram, 10);

      execTimeValue.text= '';
      pagesValue.text= '';
      deadlineValue.text= '';
      arrivalValue.text= '';
      errorProcessCreation='';
    });
  }

  //Função para informar o número de elementos da matriz de gantt
  int calculateGanttItems(){
    if(gantt.isEmpty){
      return 0;
    }
    int numberOfitems= 0;
    for(int i= 0; i<gantt.length; i++){
      numberOfitems+= gantt[i].length;
    }
    return numberOfitems;
  }

  //Função para informar o número de elemenos por linha da matriz de gantt
  int calculateGanttItemsRow(){
    if(gantt.isEmpty){
      return 1;
    }
    else{
      return gantt.length+1; //+1 para acomodar o contador de ciclo de CPU
    }
  }

  //Escolhe a cor para o gráfico
  Color pickGanttColor(int index){
    if(gantt.isEmpty){
      return Colors.transparent;
    }
    else{
      int auxRow= ganttRow;
      if(ganttRow >= gantt.length){
        ganttRow= 0;
        auxRow= 0;
        if(ganttColumn < gantt[0].length){
          ganttColumn++;
        }       
      }
      ganttRow++; 
      return ganttColors[gantt[auxRow][ganttColumn]];
    }
  }

  //Função para calcular a altura do container do gráfico de gantt
  double getGraphHeight(){
    if(gantt.isEmpty){
      return 10;
    }
    else{
      double graphHeight= gantt.length * 40;
      return graphHeight;
    }

  }

  //Função para limitar dinamicamente o gráfico de gantt até o tamanho lateral máximo
  double getGraphWidth(){
    if(gantt.isEmpty){
      return 10;
    }
    else{
      double graphWidth= gantt[0].length*40;
      if(graphWidth>1500){
        graphWidth= 1500;
      }
      return graphWidth;
    }
  }

    //Mostra o estado do processo em número no gráfico
  int showGanttState(int index){
    if(gantt.isEmpty){
      return 9;
    }
    else{
      int auxRow= ganttRow;
      if(ganttRow >= gantt.length){
        ganttRow= 0;
        auxRow= 0;
        if(ganttColumn < gantt[0].length){
          ganttColumn++;
        }       
      }
      ganttRow++;  
      return gantt[auxRow][ganttColumn]; 
    }
  }

  //Função para gerar lista de widgets para o gráfico de Gantt
  List<Widget> gridGenerateChild(){

    if(gantt.isEmpty){
      return [];
    }

    ganttRow=0;
    ganttColumn=0;
    List<Widget> generatedList= [];
    //if (switchValue == false){
      generatedList= List.generate(calculateGanttItems(), (index) => 
        Padding(
          padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
          child: Container(
            height: 1,
            width: 1,
            decoration: BoxDecoration(
              borderRadius: const BorderRadius.all(Radius.circular(8)),
              color: pickGanttColor(index),
            ),
          ),
        )
      );
    //}
    /*else{
      generatedList= List.generate(calculateGanttItems(), (index) => 
        Text(
          //'$index',
          '${showGanttState(index)}',
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        )
      );
    }*/

    //Adicionar o ciclo da cpu ao final de cada coluna
    int cpuCycle= 0;
    for (int i= gantt.length; i<generatedList.length; i+=gantt.length+1){
      generatedList.insert(i, //Coloca no index i
        Container(
            height: 1,
            width: 1,
            alignment: Alignment.center,
            decoration: const BoxDecoration(
              borderRadius: BorderRadius.all(Radius.circular(8)),
              color: Colors.transparent,
            ),
            child: Text(
                '$cpuCycle',
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w400,
              ),
            ),
        ),
      );
      cpuCycle++;
    }
    generatedList.add( //Coloca no final
      Container(
          height: 1,
          width: 1,
          alignment: Alignment.center,
          decoration: const BoxDecoration(
            borderRadius: BorderRadius.all(Radius.circular(8)),
            color: Colors.transparent,
          ),
          child: Text(
              '$cpuCycle',
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold
              ),
            ),
      ),
    );
    return generatedList;
  }

  //Cria todos os containers dos processos
  Widget getContainer(int index, List<Process> process, List<Color> processColors){
    if(gantt.isEmpty){
      return Container();
    }
    if(index < gantt.length){
      return Padding(
            padding: const EdgeInsets.fromLTRB(1, 1, 1, 1),
            child: Container(
              alignment: Alignment.center,
              height: 38,
              width: 40,
              decoration: BoxDecoration(
                borderRadius: const BorderRadius.all(Radius.circular(8)),
                color: processColors[index],
              ),
              child:Text(
                '${process[index].id}',
                style: const TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ) ,
            ),
      );
    }
    else{
      return Container();
    }
  }

}
