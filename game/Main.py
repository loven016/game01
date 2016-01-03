import sys
import pygame
from pygame import *
#import SpriteRemix
#from SpriteRemix import *
from Character import PlayerCharacterSprite
from Character import EnemyCharacterSprite
from Movement import *
from VectorMath import *
from Animation import *
from CombatText import *


'''
TODO: wrap any code doing anything which may need to be done repeatedly or in multiple places
in functions in appropriate class files.
'''
def main():
    init()
    global width, height, animator
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size, FULLSCREEN)
    gameClock = time.Clock()
    animator = Animation()
    
    #load default background
    background = pygame.sprite.Group()
    bg1 = SpriteRemix.Background(transform.scale(image.load("Assets\\backgrounds\outsidebg.png").convert(),(1920,1080)))
    bg2 = SpriteRemix.Background(transform.scale(image.load("Assets\\backgrounds\outsidebg.png").convert(),(1920,1080)))
    bg1.stateVal = 1 #slowscroll
    bg2.stateVal = 1 #slowscroll
    bg1.add(background)
    bg2.add(background)

    #load ui, TODO: encapsulate this shit
    ui = pygame.sprite.Group()
    health = SpriteRemix.UI(transform.scale(image.load("Assets\\sprites\\ui\\health.png").convert(),(596,72)))
    healthbar = SpriteRemix.UI(transform.scale(image.load("Assets\\sprites\\ui\\healthbar.png").convert_alpha(),(840,84)))
    health.add(ui)
    healthbar.add(ui)

    #create cursor and add it to a sprite group, can only hold 1 cursor at a time
    cursors = pygame.sprite.GroupSingle()
    crsr = SpriteRemix.Cursor(transform.scale(pygame.image.load("Assets\\sprites\\cursors\\crosshair1.png").convert_alpha(),(70,70)))
    crsr.add(cursors)


    #create pc and add it to a sprite group
    #TODO: need an initializer class for player that loads projectiles and weapons and shit
    pc = pygame.sprite.Group()
    playerSprite = PlayerCharacterSprite()
    animator.load(playerSprite)
    playerSprite.add(pc)
    
    #weapon, this shit is fucking retarded
    pcAccessory = pygame.sprite.Group()
    playerWeapon = SpriteRemix.Weapon()
    animator.load(playerWeapon)
    playerWeapon.add(pcAccessory)

    
    #create baddies and add them to a sprite group
    baddies = sprite.Group()
    baddySprite = EnemyCharacterSprite("notzigrunt")
    animator.load(baddySprite)
    baddySprite.add(baddies)

    #create doodads and add them to a sprite group
    doodads = sprite.Group()
    box = SpriteRemix.Doodad(pygame.image.load("Assets\\sprites\\doodads\\box.png").convert())
    #alsoBox = Doodad(pygame.image.load("Assets\\sprites\\doodads\\box.png").convert())
    box.add(doodads)
    #alsoBox.add(doodads)

    #initialize projectile sprite group (obv nothing to put here at startup
    projectiles = sprite.Group()
    
    #floating combat text
    combatTextArr = []

    #place everything
    bg1.rect.topleft = [-1920,0]
    bg2.rect.topleft = [0,0]

    healthbar.rect.topleft = [50,50]
    health.rect.topleft = [healthbar.rect.left+239, healthbar.rect.top+5]
    
    playerSprite.rect.bottomleft = [100,height-50]
    playerWeapon.rect.midright = playerSprite.rect.midleft

    baddySprite.rect.bottom = height
    baddySprite.rect.left = 960

    box.rect.left = 540
    box.rect.bottom = height
    '''alsoBox.rect.left = 920
    alsoBox.rect.bottom = height'''

    #create a list of all sprite groups
    entities = [pc.sprites(), baddies.sprites()]
    sprites = [pc, pcAccessory, baddies, doodads, projectiles, background, ui, cursors]

    while 1:

        now = time.get_ticks()
        
        #this for loop processes all inputs in the event queue
        events = pygame.event.get()
        for event in events:

            
            #close window and quit if x is clicked or esc is pressed
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit()
                sys.exit()

            #track the cursor
            if event.type == MOUSEMOTION:
                crsr.rect.centerx = event.pos[0]
                crsr.rect.centery = event.pos[1]

            #if no input is given, this remains True, animation reflects that.
            playerSprite.state["idle"] = True
            
            #only control pc if pc not dead
            #may be simplified by banning control input events when pc dies.
            if not playerSprite.state["dying"] and not playerSprite.state["dead"]:

                

                #movement d-right a-left space-jump
                if event.type == KEYUP and event.key == K_d:
                    playerSprite.rightDash = now
                    Movement.accel(playerSprite, -playerSprite.velocity[0])
                    Movement.coast(playerSprite, playerSprite.velocity[0])
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False

                if event.type == KEYUP and event.key == K_a:
                    playerSprite.leftDash = now
                    Movement.accel(playerSprite, -playerSprite.velocity[0])
                    Movement.coast(playerSprite, playerSprite.velocity[0])
                    if playerSprite.velocity[0] == 0:
                        playerSprite.state["running"] = False
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False
                    
                if event.type == KEYUP and event.key == K_SPACE:
                    playerSprite.velocity[1] = max(0,playerSprite.velocity[1])
                    playerSprite.state["jumping"] = False
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False

                if event.type == KEYDOWN and event.key == K_d:
                    if now - playerSprite.rightDash > 250:
                        Movement.accel(playerSprite, 12)
                    else:
                        Movement.accel(playerSprite, 24)
                    playerSprite.leftDash = 0
                    playerSprite.xflip = False
                    if not playerSprite.state["jumping"] and not playerSprite.state["falling"]:
                        playerSprite.state["running"] = True
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False

                if event.type == KEYDOWN and event.key == K_a:
                    if now - playerSprite.leftDash > 250:
                        Movement.accel(playerSprite, -12)
                    else:
                        Movement.accel(playerSprite, -24)
                    playerSprite.rightDash = 0
                    playerSprite.xflip = True
                    if not playerSprite.state["jumping"] and not playerSprite.state["falling"]:
                        playerSprite.state["running"] = True
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False

                if event.type == KEYDOWN and event.key == K_SPACE:
                    Movement.jump(playerSprite)
                    playerSprite.state["idle"] = False
                    playerSprite.state["jumping"] = True
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False


                #melee attack
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and now - playerSprite.lastMelee > 300:
                    playerSprite.state["attacking"] = True
                    playerSprite.last["meleed"] = now
                    playerSprite.idleTime = 0
                    playerWeapon.hostile = True
                    playerSprite.state["idle"] = False

                if event.type == MOUSEBUTTONUP and event.button == 1:
                    playerWeapon.hostile = False
                    playerSprite.state["idle"] = False
                    playerSprite.state["attacking"] = False
                
                #ranged attack
                if event.type == MOUSEBUTTONDOWN and event.button == 3 and playerSprite.ammo > 0 and now - playerSprite.lastShot > 250:
                    playerSprite.ammo -= 1
                    projLoc = [playerSprite.rect.right, playerSprite.rect.bottom-130]
                    newProj = SpriteRemix.Projectile(projLoc, event.pos, speed=45)
                    animator.load(newProj)
                    newProj.add(projectiles)
                    newProj.rect.center = projLoc
                    playerSprite.last["shot"] = now
                    playerSprite.state["shooting"] = True
                    playerSprite.idleTime = 0
                    playerSprite.state["idle"] = False

            #ragdoll pc
            else:
                playerSprite.xcoast = playerSprite.velocity[0]
                playerSprite.ycoast = playerSprite.velocity[1]
                playerSprite.velocity = [0,0]

        if playerSprite.state["idle"]:
            playerSprite.idleTime += gameClock.get_time()
            if playerSprite.idleTime >= 2000:
                playerSprite.state["idle"] = True
            elif playerSprite.idleTime >= 300:
                playerSprite.state["ready"] = True

        #baddy behavior
        '''if (now%1000 < 20) and baddySprite.stateVal != 1:
            Movement.jump(baddySprite)'''

        #replenish ammo over time
        if (now %100 < 20) and playerSprite.ammo < 4:
            playerSprite.ammo += 1

        

        #sprites move, but these moves haven't been drawn yet
        for i in range(len(sprites)-2):
            groupList = sprites[i].sprites()
            for aSprite in groupList:
                if aSprite.xcoast > 0:
                    if aSprite.xcoast > .6:
                        aSprite.xcoast += min(-aSprite.xcoast*.1,-.6)
                    else:
                        aSprite.xcoast = 0
                elif aSprite.xcoast < 0:
                    if aSprite.xcoast < -.6:
                        aSprite.xcoast += max(-aSprite.xcoast*.1,.6)
                    else:
                        aSprite.xcoast = 0
                if aSprite.ycoast > 0:
                    if aSprite.ycoast > .6:
                        aSprite.ycoast += min(-aSprite.ycoast*.1,-.6)
                    else:
                        aSprite.ycoast = 0
                elif aSprite.ycoast < 0:
                    if aSprite.ycoast < -.6:
                        aSprite.ycoast += max(-aSprite.ycoast*.1,.6)
                    else:
                        aSprite.ycoast = 0
                aSprite.rect = aSprite.rect.move([aSprite.velocity[0]+aSprite.xcoast,aSprite.velocity[1]+aSprite.ycoast])


        # keeps characters in frame and handles collisions
        resolveFrame(sprites,entities,combatTextArr)

        # position the pc's weapon
        # TODO: encapsulate this, preferably in Animation once I figure out why it wasn't working there.
        playerWeapon.state = playerSprite.state
        if playerSprite.xflip:
            if playerWeapon.state["dead"] or playerWeapon.state["idle"]:
                playerWeapon.rect.topleft = [0,0]
            elif playerWeapon.state["attacking"] or playerWeapon.state["shooting"]:
                playerWeapon.rect.midright = [playerSprite.rect.midleft[0]+8,playerSprite.rect.midleft[1]-62]
            else:
                playerWeapon.rect.midleft = [playerSprite.rect.midright[0],playerSprite.rect.midright[1]+58]
            playerWeapon.xflip = True
        else:
            if playerWeapon.state["dead"] or playerWeapon.state["idle"]:
                playerWeapon.rect.topleft = [0,0]
            elif playerWeapon.state["attacking"] or playerWeapon.state["shooting"]:
                playerWeapon.rect.midleft = [playerSprite.rect.midright[0]-8,playerSprite.rect.midright[1]-62]
            else:
                playerWeapon.rect.midright = [playerSprite.rect.midleft[0],playerSprite.rect.midleft[1]+58]
            playerWeapon.xflip = False

        # only animate characters and projectiles so far (i = 0 is pc, i = 1 is baddies, i = 3 is projectiles, i = 4 is background)
        animator.animate([sprites[0].sprites(), sprites[1].sprites(), sprites[2].sprites(), sprites[4].sprites(), sprites[5].sprites()], now)

        # refresh screen by drawing over previous frame with background
        screen.blit(bg1.image, bg1.rect)
        screen.blit(bg2.image, bg2.rect)
            
        # draw active CombatText objects and remove faded ones
        for combatText in combatTextArr[:]:
            if combatText.progress(now):
                combatText.draw(screen)
            else:
                combatTextArr.remove(combatText)

        # draw all the rest of the in-use assets
        for i in range(len(sprites)):
            if i != 5: #don't draw UI
                # only draw visible sprites in each group
                # NOTE: this is probably bad, as I'd assume .draw() (sprite method that blits all sprites in a sprite group)is better
                # optimized, but we can't make it optionally draw
                # sprites unless we change everything to DirtySprites (a type built into pygame)
                for aSprite in sprites[i].sprites():
                    if aSprite.visible:
                        screen.blit(aSprite.image,aSprite.rect)

        # draw UI last
        print(health.rect.width)
        if health.rect.width > 5.96*playerSprite.health:
            print("decreasing\n")
            health.image = transform.scale(health.image, (max(0,health.rect.width-3),health.rect.height))
            health.rect = health.image.get_rect()
            health.rect.topleft = (289,56)
        screen.blit(health.image, health.rect)
        screen.blit(healthbar.image, healthbar.rect)
        
        gameClock.tick(60)


        #game over check
        if playerSprite.health <= 0:
            defaultText = font.Font(None,120)
            gameOverSurface = defaultText.render("Game Over man, Game Over!", True, (255,0,0))
            gameOverRect = gameOverSurface.get_rect()
            gameOverRect.center = (960,540)
            screen.blit(gameOverSurface, gameOverRect)
            playerSprite.state["dead"] = True

        #victory check
        enemies = sprites[2].sprites()
        allDead = True
        for enemy in enemies:
            if enemy.stateVal != 4:
                allDead = False
        if allDead:
            defaultText = font.Font(None,200)
            conglaturationSurface = defaultText.render("Conglaturation", True, (255,255,255))
            conglaturationRect = conglaturationSurface.get_rect()
            conglaturationRect.center = (960,540)
            screen.blit(conglaturationSurface, conglaturationRect)

        pygame.display.flip()

def resolveFrame(sprites,entities,combatTextArr):
    now = time.get_ticks()
    characters = sprites[0].sprites()
    enemies = sprites[2].sprites()
    projs = sprites[4].sprites()
    weapon = sprites[1].sprites()[0]

    #melee damage to enemies
    smucked = sprite.spritecollide(weapon, enemies, False)
    for victim in smucked:
        print("SMUCKED!")
        if weapon.hostile and now - victim.lastHit > 250:
            victim.lastHit = now
            healthWas = victim.health
            victim.health -= weapon.dmg
            direction = VectorMath.normalize([victim.rect.center[0]-weapon.rect.center[0], victim.rect.center[1]-weapon.rect.center[1]])
            knockback = VectorMath.mult(direction,weapon.dmg)
            Movement.coast(victim, knockback[0], knockback[1])
            if victim.stateVal != 4:
                newCombatText = CombatText(str(min(weapon.dmg,healthWas)), victim.rect.midtop, (255,255,255), 750, 2, now)
                combatTextArr.append(newCombatText)
            if victim.health <= 0:
                victim.stateVal = 4
            

    #projectile damage to enemies
    for ind in range(len(enemies)):
        hitby = sprite.spritecollide(enemies[ind], sprites[4], False)
        if hitby and (now - entities[1][ind].lastHit > 250):
            entities[1][ind].lastHit = now
            healthWas = entities[1][ind].health
            entities[1][ind].health -= hitby[0].dmg
            enemies[ind].velocity = [0,0]
            Movement.coast(enemies[ind], hitby[0].velocity[0]/2.0, hitby[0].velocity[1]/2.0)
            if not hitby[0].piercing:
                animator.inuse[hitby[0].id] = []
                sprites[4].remove(hitby[0])
                for hitter in hitby:
                    del hitter
            #create combat text to display damage dealt
            if enemies[ind].stateVal != 4:
                newCombatText = CombatText(str(min(hitby[0].dmg,healthWas)), enemies[ind].rect.midtop, (255,255,255), 750, 2, now)
                combatTextArr.append(newCombatText)
            if entities[1][ind].health <= 0:
                enemies[ind].stateVal = 4


    #health reduction and knockback from enemy contact
    if characters[0].stateVal != 4:
        ouches = sprite.spritecollide(characters[0], sprites[2], False)
        if ouches and (now - entities[0][0].lastHit > 750):
            hurts = False
            for ouch in ouches:
                if ouch.stateVal != 4:
                    hurts = True
            if hurts:
                dmg = 10
                entities[0][0].lastHit = now
                entities[0][0].health -= dmg

                #keeps char's downward momentum from cancelling knockback if char is falling.
                characters[0].velocity[1] = 0
                baddyRect=ouches[0].rect
                #the vector from the center of the baddy to the center of the PC
                knockbackDirection = [characters[0].rect.center[0]-baddyRect.center[0],characters[0].rect.center[1]-baddyRect.center[1]]
                #converted to unit vector
                knockbackUnit = VectorMath.normalize(knockbackDirection)
                #magnified for knockback
                knockback = VectorMath.mult(knockbackUnit,40)
                Movement.coast(characters[0], knockback[0], knockback[1])            
                #create combat text to display damage dealt
                newCombatText = CombatText(str(dmg), characters[0].rect.midtop, (255,0,0), 750, 2, now)
                combatTextArr.append(newCombatText)

    #if sprite hit the ground or started on the ground, convert it's vertical momentum (ycoast) into lateral momentum (xcoast),
    #may reduce this by some constant factor later for better control feel.
    if not characters[0].state["falling"]:
        if characters[0].xcoast > 0:
            characters[0].xcoast = VectorMath.magnitude([characters[0].xcoast,abs(characters[0].ycoast)])
        if characters[0].xcoast < 0:
            characters[0].xcoast = -(VectorMath.magnitude([characters[0].xcoast,abs(characters[0].ycoast)]))
        characters[0].ycoast = 0

    #if characters[0].xcoast: print(characters[0].xcoast)#VectorMath.magnitude([characters[0].xcoast,characters[0].ycoast]))
    #physics(sprites,characters[0])

    for aSprite in characters[:1] + enemies + projs:
        physics(sprites,aSprite)

def physics(sprites,someSprite):
    #gravity (make shit fall)
    if not isinstance(someSprite, SpriteRemix.Projectile) or someSprite.grav:
        testsprite = SpriteRemix.SpriteRemix()
        testsprite.setImage(someSprite.image)
        testsprite.rect.x = someSprite.rect.x
        testsprite.rect.y = someSprite.rect.y+1
        if (not sprite.spritecollide(testsprite, sprites[3], False)) and (not testsprite.rect.bottom > height-50):
            print("whyyy\n")
            someSprite.state["falling"] = True
        del testsprite
        if someSprite.state["falling"]:
            someSprite.velocity[1] += (max(abs(someSprite.velocity[1])*.05,1.6))
        if someSprite.velocity[1] >= 0:
            someSprite.state["jumping"] = False

    #generate list of all doodads someSprite is colliding with and uncollide it with them
    collideds = sprite.spritecollide(someSprite, sprites[3], False)
    for doodad in collideds:
        #someSprite's bottom has collided while falling
        if someSprite.rect.bottom >= doodad.rect.top and someSprite.rect.bottom <= doodad.rect.top+someSprite.velocity[1]+someSprite.ycoast\
        and someSprite.state["falling"]:
            someSprite.rect.bottom = doodad.rect.top
            someSprite.numJumps = 2
            someSprite.velocity[1] = 0
            someSprite.state["falling"] = False

        elif someSprite.rect.right > doodad.rect.left and someSprite.rect.right <= doodad.rect.left+someSprite.velocity[0]+someSprite.xcoast:
            someSprite.rect.right = doodad.rect.left-1
        elif someSprite.rect.left < doodad.rect.right and someSprite.rect.left >= doodad.rect.right+someSprite.velocity[0]+someSprite.ycoast:
            someSprite.rect.left = doodad.rect.right+1

    #destroy off-screen projectiles
    if isinstance(someSprite, SpriteRemix.Projectile):
        if someSprite.rect.top > height or\
           someSprite.rect.bottom < 0 or\
           someSprite.rect.left > width or\
           someSprite.rect.right < 0:
            animator.inuse[someSprite.id] = []
            sprites[4].remove(someSprite)

    else:

        #keeps someSprite from falling off screen
        if someSprite.rect.bottom > height-50:
            someSprite.velocity[1] = 0
            someSprite.rect.bottom = height-50
            someSprite.numJumps = 2
            someSprite.state["falling"] = False

        #keeps someSprite from walking off screen
        if someSprite.rect.left < 0:
            someSprite.rect.left = 0
        elif someSprite.rect.right > width:
            someSprite.rect.right = width
