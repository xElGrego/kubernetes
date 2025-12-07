package performance

import com.intuit.karate.gatling.PreDef._
import io.gatling.core.Predef._
import scala.concurrent.duration._

class UsersSimulation extends Simulation {

  val protocol = karateProtocol()

  val users = scenario("Users API Load Test")
    .exec(karateFeature("classpath:performance/users.feature"))

  setUp(
    users.inject(
        rampUsers(10) during (10 seconds),
        constantUsersPerSec(100) during (60 seconds)
    ).protocols(protocol)
  )
}
