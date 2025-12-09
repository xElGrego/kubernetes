package performance

import com.intuit.karate.gatling.PreDef._
import io.gatling.core.Predef._
import scala.concurrent.duration._

class OrdersStressTest extends Simulation {

  val protocol = karateProtocol()

  val orders = scenario("Orders Stress Test")
    .exec(karateFeature("classpath:performance/orders.feature"))

  setUp(
    orders.inject(
      rampUsersPerSec(1) to 50 during (1.minute), // 1 Warm-up (subida suave)
      rampUsersPerSec(50) to 300 during (2.minutes), // 2 Stress ramp-up (subida fuerte)
      constantUsersPerSec(300) during (1.minute), // 3 Steady-state (carga máxima sostenida)
      rampUsersPerSec(300) to 50 during (30.seconds), // 4 Cool-down (bajar carga gradualmente)
      nothingFor(10.seconds) // 5 descanso final
    ).protocols(protocol)
  )
}
