from future.builtins import zip

import datetime
import unittest

from apel.parsers import LSFParser


class ParserLSFTest(unittest.TestCase):
    '''
    Test case for LSF parser
    '''

    def setUp(self):
        self.parser = LSFParser('testSite', 'testHost', True)

    def test_parse(self):

        fields = ('JobName', 'LocalUserID', 'LocalUserGroup', 'WallDuration',
                  'CpuDuration', 'StartTime', 'StopTime', 'MemoryReal',
                  'MemoryVirtual', 'NodeCount', 'Processors')

        lines = (
            ('"JOB_FINISH" "5.1" 1089407406 699195 283 33554482 1 1089290023 0 0 1089406862 '
             '"raortega" "8nm" "" "" "" "lxplus015" "prog/step3c" "" "/afs/cern.ch/user/r/raortega/log/bstep3c-362.txt" '
             '"/afs/cern.ch/user/r/raortega/log/berr-step3c-362.txt" "1089290023.699195" 0 1 "tbed0079" 64 3.3 "" '
             '"/afs/cern.ch/user/r/raortega/prog/step3c/startEachset.pl 362 7 8" 277.210000 17.280000 0 0 -1 0 0 927804'
             ' 87722 0 0 0 -1 0 0 0 0 0 -1 "" "default" 0 1 "" "" 0 310424 339112 "" "" ""'),
            # MPI information
            ('"JOB_FINISH" "7.06" 1302184020 436491 10001 33816691 16 1302184001 0 0 1302184004 "viglen" "normal" '
             '" span[ptile=8] cu[maxcus=1]" "" "" "comp000" "benchmarks/IMB_3.0/bin/bsub" "" "IMB.%J.%I.out" '
             '"IMB.%J.%I.err" "1302184001.436491" 0 16 "comp042" "comp042" "comp042" "comp042" "comp042" "comp042" '
             '"comp042" "comp042" "comp043" "comp043" "comp043" "comp043" "comp043" "comp043" "comp043" "comp043" 32'
             ' 60.0 "imb_sr[1-90]" "#!/bin/bash; #BSUB -n 16;#BSUB -R \'span[ptile=8]\';#BSUB -R \'cu[maxcus=1]\';#BSUB '
             '-x;#BSUB -J imb_sr[1-90];####BSUB -m ""comp000 comp001"";#BSUB -o IMB.%J.%I.out;#BSUB -e IMB.%J.%I.err; '
             '# Output some env vars;echo ""LSB_HOSTS: $LSB_HOSTS"";echo ""LSB_MCPU_HOSTS: $LSB_MCPU_HOSTS"";echo '
             '""LSB_DJOB_HOSTFILE: $LSB_DJOB_HOSTFILE"";echo ""LSB_DJOB_HOSTFILE (cat):""; cat $LSB_DJOB_HOSTFILE; '
             'HOSTLIST=`cat $LSB_DJOB_HOSTFILE | uniq | tr ""\n"" "" ""`; . /etc/profile; module add MPI/PMPI;cd '
             '/home/test/viglen/benchmarks/IMB_3.0/bin/ ;#mpirun -np $LSB_DJOB_NUMPROC ./imb-pmpi -msglen ./IMB_msglen '
             '-map 2x8 -npmin 16 sendrecv;#mpirun -d -prot -np $LSB_DJOB_NUMPROC -hostlist ""comp000 comp001"" '
             './imb-pmpi -msglen ./IMB_msglen -map 2x8 -npmin 16 sendrecv;mpirun -d -prot -np $LSB_DJOB_NUMPROC '
             '-hostlist ""$HOSTLIST"" ./imb-pmpi -msglen ./IMB_msglen -map 2x8 -npmin 16 sendrecv" 0.472928 1.112830 '
             '0 0 -1 0 0 149746 0 0 0 0 -1 0 0 0 1907 1746 -1 "" "default" 65280 16 "" "" 23 2 25 "" "" "" "" 0 "" 0 ""'
             ' -1 "/viglen" "" "default" "" -1 "" "" 6160  "" 1302184004 "" "" 0'),
            # LSF 9 log (Mixed quotes used to handle mixed quotes in string)
            ('"JOB_FINISH" "9.11" 1380043655 31255091 386919 36175899 1 1380043614 0 0 1380043630 "oops17" "abcgrid" '
             '"" "" "" "nice.phys.abc-uni.uk" "" "/dev/null" "/dev/null" "" "191/1380043614.31255091" 0 1 "a0052" 64 '
             '78.0 "cream_123456789" "#!/bin/bash;# LSF job wrapper generated by lsf_submit.sh;# on Tue Sep 24 19:2'
             '6:51 CEST 2013;#;# LSF directives:;#BSUB -L /bin/bash;#BSUB -J cream_123456789;#BSUB -q abcgrid;#BSUB -n'
             '1;#BSUB -f ""/var/cream_sandbox/ops/CN_Robot__grid_client___Someone_Somewhere'
             'NGI_Somewhere_Role_NULL_Capability_NULL_ops017/18/CREAM123456789/CREAM123456789_jobWrapper.sh > CREAM18173'
             '0262_jobWrapper.sh.386919.7105.1380043611"";#BSUB -f ""/var/cream_sandbox/ops/CN_Robot__grid_client___So'
             'meone_Somewhere/proxy/426e0fbced998f1b9162bb6a0db0eeedc2c_18361079272219 > cream_123456789.proxy"";#BSUB'
             '-f ""/var/cream_sandbox/ops/CN_Robot__grid_client___Someone_Somewhere/18/CREAM123456789/StandardOutput <'
             'out_cream_123456789_StandardOutput"";#BSUB -f ""/var/cream_sandbox/ops/CN_Robot__grid_client___Someone_S'
             'omewhere/18/CREAM123456789/StandardError < err_cream_181730262_StandardError""; # Check whet'
             'her we need to move to the LSF original CWD:;if [ -d ""$CERN_STARTER_ORIGINAL_CWD"" ]; then;    cd $CERN'
             '_STARTER_ORIGINAL_CWD;fi;old_home=`pwd`;new_home=${old_home}/home_cream_123456789;mkdir $new_home;trap '
             "'wait $job_pid; cd $old_home; rm -rf $new_home; exit 255' 1 2 3 15 24;trap 'wait $job_pid; cd $old_home;"
             "rm -rf $new_home' 0;# Copy into new home any shared input sandbox file;# Move into new home any relative"
             'input sandbox file;mv ""CREAM123456789_jobWrapper.sh.386919.7105.1380043611"" ""$new_home/CREAM123456789'
             '_jobWrapper.sh"" &> /dev/null;mv ""cream_123456789.proxy"" ""$new_home/cream_123456789.proxy"" &> /dev/n'
             'ull;export HOME=$new_home;cd $new_home;# Resetting proxy to local position;export X509_USER_PROXY=$new_h'
             'ome/cream_123456789.proxy; # Command to execute:;if [ ! -x ./CREAM123456789_jobWrapper.sh ]; then chmod '
             'u+x ./CREAM123456789_jobWrapper.sh; fi;if [ -x ${GLITE_LOCATION:-/opt/glite}/libexec/jobwrapper ];then;$'
             '{GLITE_LOCATION:-/opt/glite}/libexec/jobwrapper ./CREAM123456789_jobWrapper.sh  > ""out_cream_123456789_'
             'StandardOutput"" 2> ""err_cream_123456789_StandardError"" & elif [ -x /opt/lcg/libexec/jobwrapper ];then'
             ';/opt/lcg/libexec/jobwrapper ./CREAM123456789_jobWrapper.sh  > ""out_cream_123456789_StandardOutput"" 2>'
             '""err_cream_123456789_StandardError"" & elif [ -x $BLAH_AUX_JOBWRAPPER ];then;$BLAH_AUX_JOBWRAPPER ./CRE'
             'AM123456789_jobWrapper.sh  > ""out_cream_123456789_StandardOutput"" 2> ""err_cream_123456789_StandardErr'
             'or"" & else;$new_home/CREAM123456789_jobWrapper.sh  > ""out_cream_123456789_StandardOutput"" 2> ""err_cr'
             'eam_123456789_StandardError"" & fi;job_pid=$!; # Wait for the user job to finish;wait $job_pid;user_retc'
             'ode=$?; # Move all relative outputsand paths out of temp home;cd $new_home;mv ""out_cream_123456789_Stan'
             'dardOutput"" ""$old_home/out_cream_123456789_StandardOutput"" 2> /dev/null;mv ""err_cream_123456789_Stan'
             'dardError"" ""$old_home/err_cream_123456789_StandardError"" 2> /dev/null;# Move any remapped outputsand '
             'file to shared directories; # Remove the staged files, if any;rm ""CREAM123456789_jobWrapper.sh"" 2> /de'
             'v/null;rm ""cream_123456789.proxy"" 2> /dev/null;cd $old_home; exit $user_retcode" 15.093705 8.511706 52'
             '96 0 -1 0 0 26452 0 0 0 16 -1 0 0 0 242 171 -1 "" "default" 0 1 "/bin/bash" "" 0 1495304 0 "" "" "" "" 0'
             '"" 0 "" -1 "/ops/ops017" "" "" "" -1 "" "" 6160 "" 1380043630 "" "" 0 0 -1 0 441780 "select[ type == any'
             '] order[-ut] rusage[r1m=0.91:duration=2m:decay=0] " "" -1 "" -1 0 "" 0 0 "" 25 "" 0 ""'))

        values = (
            ('699195', 'raortega', None, 544, 294,
             datetime.datetime.utcfromtimestamp(1089406862),
             datetime.datetime.utcfromtimestamp(1089407406),
             310424, 339112, 1, 1),
            ('436491', 'viglen', None, 16, 2,
             datetime.datetime.utcfromtimestamp(1302184004),
             datetime.datetime.utcfromtimestamp(1302184020),
             2, 25, 2, 16),
            ('31255091', 'oops17', None, 25, 24,
             datetime.datetime.utcfromtimestamp(1380043630),
             datetime.datetime.utcfromtimestamp(1380043655),
             1495304, 0, 1, 1))

        cases = {}
        for line, value in zip(lines, values):
            cases[line] = dict(zip(fields, value))

        for line in list(cases.keys()):

            record = self.parser.parse(line)
            cont = record._record_content

            self.assertEqual(cont['Site'], 'testSite')
            self.assertEqual(cont['MachineName'], 'testHost')
            self.assertEqual(cont['Infrastructure'], 'APEL-CREAM-LSF')

            for field in list(cases[line].keys()):
                self.assertIn(field, cont, "Field '%s' not in record: %s" % (field, cont))

            for key in list(cases[line].keys()):
                self.assertEqual(cont[key], cases[line][key], "%s != %s for key %s" % (cont[key], cases[line][key], key))

    def test_invalid_expr(self):
        # two fields are not separated by space
        line = ('"JOB_FINISH" "5.1" 1089407406 699195 283 33554482 1 1089290023 0 0 1089406862 '
                '"raortega" "8nm" "" "" "" "lxplus015" "prog/step3c" "" "/afs/cern.ch/user/r/raortega/log/bstep3c-362.txt" '
                '"/afs/cern.ch/user/r/raortega/log/berr-step3c-362.txt""1089290023.699195" 0 1 "tbed0079" 64 3.3 "" '
                '"/afs/cern.ch/user/r/raortega/prog/step3c/startEachset.pl362 7 8" 277.210000 17.280000 0 0 -1 0 0 927804'
                ' 87722 0 0 0 -1 0 0 0 0 0 -1 "" "default" 0 1 "" "" 0 310424 339112 "" "" ""')

        self.assertRaises(IndexError, self.parser.parse, line)

    def test_wall_value_error(self):
        """Check that stop before start raises a ValueError."""
        line = ('"JOB_FINISH" "5.1" 1089407406 699195 283 33554482 1 1089290023'
                ' 0 0 1089409862 "raortega" "8nm" "" "" "" "lxplus015" "prog/st'
                'ep3c" "" "/step3c-362.txt" "/berr-step3c-362.txt" "1089290023.'
                '699195" 0 1 "tbed0079" 64 3.3 "" "/artEachset.j 362 7 8" 277.2'
                '10000 17.280000 0 0 -1 0 0 927804 87722 0 0 0 -1 0 0 0 0 0 -1 '
                '"" "default" 0 1 "" "" 0 310424 339112 "" "" ""')
        self.assertRaises(ValueError, self.parser.parse, line)

    def test_unfinished(self):
        """Check that a valid line without JOB_FINISH returns None."""
        line = ('"JOB_RESIZE" "5.1" 1089407406 699195 283 33554482 1 1089290023'
                ' 0 0 1089406862 "raortega" "8nm" "" "" "" "lxplus015" "prog/st'
                'ep3c" "" "/step3c-362.txt" "/berr-step3c-362.txt" "1089290023.'
                '699195" 0 1 "tbed0079" 64 3.3 "" "/artEachset.j 362 7 8" 277.2'
                '10000 17.280000 0 0 -1 0 0 927804 87722 0 0 0 -1 0 0 0 0 0 -1 '
                '"" "default" 0 1 "" "" 0 310424 339112 "" "" ""')

        self.assertEqual(self.parser.parse(line), None)

    def test_non_mpi(self):
        """Test that node and cpu count are set to zero if MPI isn't used."""
        parser = LSFParser('testSite', 'testHost', False)

        line = ('"JOB_FINISH" "5.1" 1089407406 699195 283 33554482 1 1089290023'
                ' 0 0 1089406862 "raortega" "8nm" "" "" "" "lxplus015" "prog/st'
                'ep3c" "" "/af/step3c-362.txt" "/af/epc-362.txt" "1089290023.69'
                '9195" 0 1 "tbed0079" 64 3.3 "" "/af/hset.pl 362 7 8" 277.2100 '
                '17.280000 0 0 -1 0 0 927804 87722 0 0 0 -1 0 0 0 0 0 -1 "" "de'
                'fault" 0 1 "" "" 0 310424 339112 "" "" ""')

        record = parser.parse(line)
        cont = record._record_content

        self.assertEqual(cont['NodeCount'], 0,
                          "Node count not zero for non-mpi parser")
        self.assertEqual(cont['Processors'], 0,
                          "Processors not zero for non-mpi parser")


if __name__ == '__main__':
    unittest.main()
