#****************************************************************************
#
# Makefile for CProcModule.
# www.srplab.com
#****************************************************************************
DEBUG          := YES
PROFILE        := NO
#****************************************************************************
CC     := gcc
CXX    := g++
LD     := g++
AR     := ar
RANLIB := ranlib
		
DEBUG_CFLAGS     := -Wall -Wno-format -g -DDEBUG -DENV_MACOS
RELEASE_CFLAGS   := -Wall -Wno-unknown-pragmas -Wno-format -O3 -DENV_MACOS
				  
LIBS	:= -ldl -lpthread -L/usr/local/lib -lstarlib
EXTRA_LIBS := 
			
DEBUG_CXXFLAGS   := ${DEBUG_CFLAGS} 
RELEASE_CXXFLAGS := ${RELEASE_CFLAGS}
				  
DEBUG_LDFLAGS    := -g
RELEASE_LDFLAGS  :=
				  
ifeq (YES, ${DEBUG})
    CFLAGS       := ${DEBUG_CFLAGS}
    CXXFLAGS     := ${DEBUG_CXXFLAGS}
    LDFLAGS      := ${DEBUG_LDFLAGS}
else
    CFLAGS       := ${RELEASE_CFLAGS}
    CXXFLAGS     := ${RELEASE_CXXFLAGS}
    LDFLAGS      := ${RELEASE_LDFLAGS}
endif
ifeq (YES, ${PROFILE})
    CFLAGS   := ${CFLAGS} -pg -O3
    CXXFLAGS := ${CXXFLAGS} -pg -O3
    LDFLAGS  := ${LDFLAGS} -pg
endif
#****************************************************************************
# Makefile code common to all platforms
#****************************************************************************
CFLAGS   := ${CFLAGS}   ${DEFS}
CXXFLAGS := ${CXXFLAGS} ${DEFS}
#****************************************************************************
# include source and paths
#****************************************************************************
INCS_T := /usr/local/include/starcore
INCS   = $(addprefix -I,$(INCS_T))
CProcModule_CXXSRCS := ../CProcModule_main.cpp
#****************************************************************************
CProcModule_CXXOBJS := $(CProcModule_CXXSRCS:%.cpp=%.o)
#****************************************************************************
CXXOBJS := ${CProcModule_CXXOBJS}
COBJS := 
ShareLib_CProcModule_OBJS := ${CProcModule_CXXOBJS}
#****************************************************************************
# Targets of the build
#****************************************************************************
OBJS_PATH = ../
ShareLib_CProcModule := ${OBJS_PATH}/CProcModule.dylib
all: ${ShareLib_CProcModule}
#****************************************************************************
# Output
#****************************************************************************
${ShareLib_CProcModule}: ${ShareLib_CProcModule_OBJS}
	${LD} -shared -o $@ ${LDFLAGS} ${ShareLib_CProcModule_OBJS} ${LIBS} ${EXTRA_LIBS}
#****************************************************************************
# common rules
#****************************************************************************
${CXXOBJS} :
	${CXX} -fPIC -fno-strict-aliasing ${CXXFLAGS} ${INCS} $< -o $@ -c $*.cpp
${COBJS} : 
	${CC} -fPIC -fno-strict-aliasing ${CFLAGS} ${INCS} -o $@ -c $*.c
clean:
	-rm -f core ${CXXOBJS} ${COBJS} ${ShareLib_CProcModule}
