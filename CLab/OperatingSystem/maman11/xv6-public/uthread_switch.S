	.text

/* Switch from current_thread to next_thread. Make next_thread
 * the current_thread, and set next_thread to 0.
 * Use eax as a temporary register, which should be caller saved.
 */
	.globl thread_switch
thread_switch:

	pushal /* push the 8 register to 8*4=32 bytes of the sp->stack (current_thread-> stack) */

	movl current_thread, %eax /* ax = current_thread*/
	movl %esp, (%eax)         /* ax->sp = sp*/

	movl next_thread, %eax    /* ax = next_thread */
	movl (%eax), %esp         /* sp = ax->sp */

	/* Set current_thread to next_thread */
	movl %eax, current_thread /* current_thread = ax; //current_thread = next_thread */

	
	popal /* pop to the 8 register the 8*4=32 last bytes of the next_thread that it is data and now the sp reg point to next_thread*/

	movl $0, next_thread      /* next_thread = 0; //next_thread = null*/

	ret /* pop return address from stack */
