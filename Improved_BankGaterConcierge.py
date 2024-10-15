# Improved version of MeesaJarJar's BankGaterConcierge script brough to you by Moruk
# This script gates automatically for people when they request a gate via the GateCommand
# This helps save gold and resources on wasted gates that no one uses. 

# Settings: Change these to fit your needs!
target = Target.PromptTarget("Select a recall rune or a runebook with Default Rune Set", 0)  # Set to the runebook with the desired location or a recall rune.
GateCommand = "!gate"  # Command players use to request a gate.
minTimePerGateRequest = 60000  # Limits players to one gate request per minute.

# Gate response messages
line1 = "Need a gate to the newest vendor in town?"
line2 = " "
line3 = "Just say !gate and I will gate you, On Demand gating."
GateCommandResponse = "Gating now, thank you for visiting us!"
LowManaResponse = "Sorry, low on mana. Meditating, then I can gate!"

# Chat settings
chatColor = 53 
timeBetweenSpam = 10000

Journal.Clear()
totalGates = 0

def handleGateRequest(playerName, totalGates):
    if Timer.Check(playerName):  # Check if the player is on cooldown
        remainingTime = round(Timer.Remaining(playerName) / 1000)
        message = f"Sorry, {playerName} can request another gate in {remainingTime} seconds."
        Misc.SendMessage(message)
        Player.ChatSay(37, message)
    else:
        if Player.Mana < 40:
            Player.ChatSay(53, LowManaResponse)
            Player.UseSkill("Meditation")
            while Player.Mana < 40:
                Misc.Pause(1000)
        Spells.CastMagery("Gate Travel")
        Player.ChatSay(62, GateCommandResponse)
        Target.WaitForTarget(60000, False)
        Target.TargetExecute(target)
        totalGates += 1
        Timer.Create(playerName, minTimePerGateRequest) 
    return totalGates

Timer.Create('spamTimer', 1000)

while True:
    Misc.Pause(1000)
    
    if not Timer.Check('spamTimer'):
        Misc.SendMessage(f"Total Gates: {totalGates}")
        for line in [line1, line2, line3]:
            Player.ChatSay(chatColor, line)
            Misc.Pause(2000)
        Timer.Create('spamTimer', timeBetweenSpam)
    
    lineAndName = Journal.GetLineText(GateCommand, True)
    
    if lineAndName:
        playerName = lineAndName.split(':')[0]
        if playerName != Player.Name: 
            totalGates = handleGateRequest(playerName, totalGates)
    
    Journal.Clear()
