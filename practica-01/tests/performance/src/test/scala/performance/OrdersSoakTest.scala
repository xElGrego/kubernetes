package performance

import com.intuit.karate.gatling.PreDef._
import io.gatling.core.Predef._
import scala.concurrent.duration._

class OrdersSoakTest extends Simulation {

  val protocol = karateProtocol()

  val orders = scenario("Orders Soak Test")
    .exec(karateFeature("classpath:performance/orders.feature"))

  setUp(
    orders.inject(

      // 1) Warm-up suave (evita falsos fallos por frío)
      rampUsersPerSec(1) to 20 during (1 minute),

      // 2) Soak load (carga constante moderada)
      constantUsersPerSec(20) during (10 minutes),

      // 3) Stress ligero en mitad del soak
      rampUsersPerSec(20) to 50 during (1 minute),
      constantUsersPerSec(50) during (2 minutes),

      // 4) Vuelta a carga normal para ver degradación
      constantUsersPerSec(20) during (5 minutes),

      // 5) Cool-down (para ver recuperación)
      rampUsersPerSec(20) to 1 during (30 seconds),

      nothingFor(10 seconds)
    ).protocols(protocol)
  )
}
