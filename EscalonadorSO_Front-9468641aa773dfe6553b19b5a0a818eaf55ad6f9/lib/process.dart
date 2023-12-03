class Process{
    int id;
    int arrivalTime;
    int execTime;
    int deadline;
    int numberOfPages;

    Process({
      required this.id,
      required this.arrivalTime,
      required this.execTime,
      required this.deadline,
      required this.numberOfPages
    });

    Map toJson() => {
      'id': id,
      'arrivalTime': arrivalTime,
      'execTime': execTime,
      'deadline': deadline,
      'numberOfPages': numberOfPages
    };

}