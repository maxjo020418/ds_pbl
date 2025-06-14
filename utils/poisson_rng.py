import numpy as np
from scipy.stats import norm, poisson, rv_discrete

class TruncatedLayeredPoissonRNG:
    def __init__(
        self,
        init_lambda: float,
        normal_params: list[tuple[float, float]],
        lower: int,
        upper: int,
        update_interval: int = 100
    ):
        """
        init_lambda     : initial Poisson rate
        normal_params   : list of (mu, sigma) tuples for λ-layer normals
        lower, upper    : integer bounds for the output (inclusive)
        update_interval : redraw λ every this many samples
        """
        if lower < 0 or upper < lower:
            raise ValueError("Require 0 ≤ lower ≤ upper")
        self.normal_params = normal_params
        self.lower = lower
        self.upper = upper
        self.update_interval = update_interval
        self.lambda_ = init_lambda
        self._count = 0
        self._build_poisson_rv()

    def _build_poisson_rv(self):
        # support is integers from lower to upper
        k = np.arange(self.lower, self.upper + 1)
        raw_pmf = poisson.pmf(k, mu=self.lambda_)
        pmf = raw_pmf / raw_pmf.sum()  # truncate & normalize
        self.poisson_rv = rv_discrete(name="trunc_pois",
                                      values=(k, pmf))

    def _update_lambda(self):
        draws = [norm(mu, sigma).rvs()
                 for mu, sigma in self.normal_params]
        self.lambda_ = max(0.0, sum(draws))
        self._build_poisson_rv()

    def sample(self) -> int:
        """
        Return one draw in [lower, upper]. Every update_interval
        calls, λ is re-drawn and the PMF re-built.
        """
        if self._count and self._count % self.update_interval == 0:
            self._update_lambda()
        self._count += 1
        return int(self.poisson_rv.rvs())

# Example
if __name__ == "__main__":
    rng = TruncatedLayeredPoissonRNG(
        init_lambda=4.0,
        normal_params=[(3.0, 1.0), (2.0, 0.5)],
        lower=0,
        upper=3,
        update_interval=50
    )
    samples = [rng.sample() for _ in range(200)]
    print(samples[:20])
