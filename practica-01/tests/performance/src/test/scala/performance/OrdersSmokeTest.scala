package performance

import com.intuit.karate.gatling.PreDef._
import io.gatling.core.Predef._
import scala.concurrent.duration._

class OrdersSmokeTest extends Simulation {

  val protocol = karateProtocol()

  val smoke = scenario("Orders Smoke Test")
    .exec(karateFeature("classpath:performance/orders.feature"))

  setUp(
    smoke.inject(
      atOnceUsers(1),                           // una ejecución inmediata
      rampUsers(3) during (5 seconds)           // sube a 3 usuarios en 5 segundos
    ).protocols(protocol)
  )
}
