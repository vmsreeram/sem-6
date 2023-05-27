package in.iitpkd.scala
import org.apache.spark._
import org.apache.log4j._

object Test2Assignment {
  def main(args: Array[String]) {
    Logger.getLogger("org").setLevel(Level.ERROR)
    val sc = new SparkContext("local[*]", "RatingsCounter")


    // Read the input file and create an RDD
    val input = sc.textFile("/Users/ajaikumarmp/Downloads/2022.07_WAVES-ACCESS-RECORDS.csv")    // Please change the path appropriately for testing

    // Extract the header and remove it from the RDD
    val header = input.first()
    val data = input.filter(row => row != header)

    // (i) 10 most frequent visitors
    val visitors = data.map(row => {
      val tokens = row.split(",")
      ((tokens(0), tokens(1), tokens(2)), 1)
    })
    val mostFrequentVisitors = visitors.reduceByKey(_ + _).sortBy(_._2, ascending = false).take(10)
    println("10 most frequent visitors:")
    mostFrequentVisitors.foreach(println)

    // (ii) 10 most frequently visited people
    val visitees = data.map(row => {
      val tokens = row.split(",")
      ((tokens(19), tokens(20)), 1)
    })
    val mostFrequentVisitees = visitees.reduceByKey(_ + _).sortBy(_._2, ascending = false).take(10)
    println("10 most frequently visited people:")
    mostFrequentVisitees.foreach(println)

    // (iii) 10 most frequent visitor-visitee combinations
    val visitorVisitee = data.map(row => {
      val tokens = row.split(",")
      (((tokens(0), tokens(1), tokens(2)), (tokens(19), tokens(20))), 1)
    })
    val mostFrequentVisitorVisitee = visitorVisitee.reduceByKey(_ + _).sortBy(_._2, ascending = false).take(10)
    println("10 most frequent visitor-visitee combinations:")
    mostFrequentVisitorVisitee.foreach(println)

    // (iv) Highest appointments made according to APPT_MADE_DATE
    val appointments = data.map(row => {
      val tokens = row.split(",")
      (tokens(10), 1)
    })
    val highestAppointments = appointments.reduceByKey(_ + _).sortBy(_._2, ascending = false).first()
    println(s"Highest appointments made on date: ${highestAppointments._1} with count: ${highestAppointments._2}")

    // (v) Percentage of tour visitors
    val totalVisitors = data.count()
    val tourVisitors = data.filter(row => row.split(",")(22) == "EW TOUR").count()
    val tourVisitorPercentage = (tourVisitors.toFloat / totalVisitors.toFloat) * 100
    println(s"Percentage of tour visitors: $tourVisitorPercentage%")

    // Stop the Spark context
    sc.stop()
  }
}
