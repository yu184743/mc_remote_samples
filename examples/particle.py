from mc_remote.minecraft import Minecraft
import param_mc_remote as param
from param_mc_remote import PLAYER_ORIGIN as PO
from param_mc_remote import block
import mc_remote.entity_1_21_5 as entity
import mc_remote.particle_1_21_5 as particle
# Connect to minecraft and open a session as player with origin location
mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
mc.setPlayer(param.PLAYER_NAME, PO.x, PO.y, PO.z)
x = 5
y = 68
z = 5
mc.spawnParticle(x,y,z,1,1,1,particle.FALLING_DRIPSTONE_LAVA,1,3000)
mc.spawnParticle(x,y,z,1,1,1,particle.FALLING_DRIPSTONE_WATER,1,3000)
mc.spawnParticle(x,y,z,1,1,1,particle.FIREWORK,1,3000)
#mc.spawnEntity(x,y,z,entity.ENDER_DRAGON)

##result = mc.spawnParticle(x, y, z, 1, 1, 1, particle.DRAGON_BREATH, 0.2, 30000)
##print(result)