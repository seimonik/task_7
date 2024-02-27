from simulation import Simulation

if __name__ == '__main__':
    mu1 = 2
    mu2 = 5
    lambd = 1
    simulation_time = 10000
    t = 7

    Simulation.run(mu1=mu1,
                   mu2=mu2,
                   lambd=lambd,
                   t=t)
