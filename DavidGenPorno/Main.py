import sys
import pygame
from pygame import *
#import SpriteRemix
#from SpriteRemix import *
from Character import *
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
    defaultSprite = image.load("Assets\\sprites\\default.png")
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
    playerSprite = SpriteRemix.PCSprite(defaultSprite, "pc")
    animator.load(playerSprite)
    player = PlayerCharacter(playerSprite)
    player.sprite.add(pc)
    
    #weapon, this shit is fucking retarded
    pcAccessory = pygame.sprite.Group()
    playerWeapon = SpriteRemix.PCSprite(defaultSprite, "weapon")
    animator.load(playerWeapon)
    playerWeapon.add(pcAccessory)

    
    #create baddies and add them to a sprite group
    baddies = sprite.Group()
    baddySprite = SpriteRemix.CharacterSprite(defaultSprite,"notzigrunt")
    animator.load(baddySprite)
    baddy = NPC(baddySprite)
    baddy.sprite.add(baddies)

    #create doodads and add them to a sprite group
    doodads = sprite.Group()
    '''box = Doodad(pygame.image.load("Assets\\sprites\\doodads\\box.png").convert())
    alsoBox = Doodad(pygame.image.load("Assets\\sprites\\doodads\\box.png").convert())
    box.add(doodads)
    alsoBox.add(doodads)'''

    #initialize projectile sprite group (obv nothing to put here at startup
    projectiles = sprite.Group()
    
    #floating combat text
    combatTextArr = []

    #place everything
    bg1.rect.topleft = [-1920,0]
    bg2.rect.topleft = [0,0]

    healthbar.rect.topleft = [50,50]
    health.rect.topleft = [healthbar.rect.left+239, healthbar.rect.top+5]
    
    player.sprite.rect.bottomleft = [100,height-50]
    playerWeapon.rect.midright = player.sprite.rect.midleft

    baddy.sprite.rect.bottom = height
    baddy.sprite.rect.left = 960

    '''box.rect.left = 540
    box.rect.bottom = height
    alsoBox.rect.left = 920
    alsoBox.rect.bottom = height'''

    #create a list of all sprite groups
    entities = [[player],[baddy]]
    sprites = [pc, pcAccessory, baddies, doodads, projectiles, background, ui, cursors]

    while 1:

        now = time.get_ticks()
        
        #this for loop processes all inputs in the event queue
        for event in pygame.event.get():

            #close window and quit if x is clicked or esc is pressed
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit()
                sys.exit()

            #track the cursor
            if event.type == MOUSEMOTION:
                crsr.rect.centerx = event.pos[0]
                crsr.rect.centery = event.pos[1]

            #only control pc if pc not dead
            if player.sprite.stateVal != 4:
                
                #fire projectiles
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and player.ammo > 0 and now - player.sprite.lastShot > 250:
                    player.ammo -= 1
                    projLoc = [player.sprite.rect.right, player.sprite.rect.bottom-130]
                    newProj = SpriteRemix.Projectile(defaultSprite, projLoc, event.pos, speed=45)
                    animator.load(newProj)
                    newProj.add(projectiles)
                    newProj.rect.center = projLoc
                    player.sprite.lastShot = now


                #movement d-right a-left space-jump
                if event.type == KEYUP and event.key == K_d:
                    player.sprite.rightDash = now
                    Movement.accel(player.sprite, -player.sprite.velocity[0])
                    Movement.coast(player.sprite, player.sprite.velocity[0])

                if event.type == KEYUP and event.key == K_a:
                    player.sprite.leftDash = now
                    Movement.accel(player.sprite, -player.sprite.velocity[0])
                    Movement.coast(player.sprite, player.sprite.velocity[0])

                if event.type == KEYDOWN and event.key == K_d:
                    if now - player.sprite.rightDash > 250:
                        Movement.accel(player.sprite, 12)
                    else:
                        Movement.accel(player.sprite, 24)
                    player.sprite.leftDash = 0
                    player.sprite.xflip = False

                if event.type == KEYDOWN and event.key == K_a:
                    if now - player.sprite.leftDash > 250:
                        Movement.accel(player.sprite, -12)
                    else:
                        Movement.accel(player.sprite, -24)
                    player.sprite.rightDash = 0
                    player.sprite.xflip = True

                if event.type == KEYDOWN and event.key == K_SPACE:
                    Movement.jump(player.sprite)

            #ragdoll pc
            else:
                player.sprite.xcoast = player.sprite.velocity[0]
                player.sprite.ycoast = player.sprite.velocity[1]
                player.sprite.velocity = [0,0]

        #baddy behavior
        '''if (now%1000 < 20) and baddy.sprite.stateVal != 1:
            Movement.jump(baddy.sprite)'''

        #replenish ammo over time
        if (now %100 < 20) and player.ammo < 4:
            player.ammo += 1

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


        #display the player's health
        """
        defaultText = font.Font(None,100)
        healthTextSurface = defaultText.render("Player health: " + str(player.health), True, (255,0,0))
        healthTextRect = healthTextSurface.get_rect()
        healthTextRect.top = 50
        healthTextRect.left = 50
        """


        #keeps characters in frame and handles collisions
        resolveFrame(sprites,entities,combatTextArr)

        #refresh screen by drawing over previous frame with background
        screen.blit(bg1.image, bg1.rect)
        screen.blit(bg2.image, bg2.rect)


        #position the pc's weapon
        if player.sprite.xflip:
            sprites[1].sprites()[0].rect.midleft = [player.sprite.rect.midright[0],player.sprite.rect.midright[1]+58]
            sprites[1].sprites()[0].xflip = True
        else:
            sprites[1].sprites()[0].rect.midright = [player.sprite.rect.midleft[0],player.sprite.rect.midleft[1]+58]
            sprites[1].sprites()[0].xflip = False

        #only animate characters and projectiles so far (i = 0 is pc, i = 1 is baddies, i = 3 is projectiles, i = 4 is background)
        animator.animate([sprites[0].sprites(), sprites[1].sprites(), sprites[2].sprites(), sprites[4].sprites(), sprites[5].sprites()], now)
            
        #draw active CombatText objects and remove faded ones
        for combatText in combatTextArr[:]:
            if combatText.progress(now):
                combatText.draw(screen)
            else:
                combatTextArr.remove(combatText)

        #draw all the rest of the in-use assets
        for i in range(len(sprites)):
            if i != 5: #don't draw UI
                sprites[i].draw(screen)

        #draw UI last
        #screen.blit(healthTextSurface, healthTextRect)
        if health.rect.width > 596*player.health/100:
            health.image = transform.scale(health.image, (max(0,health.rect.width-3),health.rect.height))
            health.rect = health.image.get_rect()
            health.rect.topleft = (289,56) #tempHealthTopLeft
        screen.blit(health.image, health.rect)
        screen.blit(healthbar.image, healthbar.rect)
        
        gameClock.tick(60)


        #game over check
        if player.health <= 0:
            defaultText = font.Font(None,120)
            gameOverSurface = defaultText.render("Game Over man, Game Over!", True, (255,0,0))
            gameOverRect = gameOverSurface.get_rect()
            gameOverRect.center = (960,540)
            screen.blit(gameOverSurface, gameOverRect)
            player.sprite.stateVal = 4

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
    if not characters[0].falling:
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
        testsprite = SpriteRemix.SpriteRemix(someSprite.image)
        testsprite.rect.x = someSprite.rect.x
        testsprite.rect.y = someSprite.rect.y
        testsprite.rect = testsprite.rect.move([0,1])
        if (not sprite.spritecollide(testsprite, sprites[2], False)) and (not testsprite.rect.bottom > height-50):
            someSprite.falling = True
        del testsprite
        if someSprite.falling == True:
            someSprite.velocity[1] += (max(abs(someSprite.velocity[1])*.05,1.6))

    #generate list of all doodads someSprite is colliding with and uncollide it with them
    collideds = sprite.spritecollide(someSprite, sprites[3], False)
    for doodad in collideds:
        #someSprite's bottom has collided while falling
        if someSprite.rect.bottom > doodad.rect.top and someSprite.rect.bottom <= doodad.rect.top+someSprite.velocity[1]+someSprite.ycoast\
        and someSprite.falling :
            someSprite.rect.bottom = doodad.rect.top
            someSprite.numJumps = 2
            someSprite.velocity[1] = 0
            someSprite.falling = False

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
            someSprite.falling = False

        #keeps someSprite from walking off screen
        if someSprite.rect.left < 0:
            someSprite.rect.left = 0
        elif someSprite.rect.right > width:
            someSprite.rect.right = width
