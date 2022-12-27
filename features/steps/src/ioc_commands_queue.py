import queue
import time

from loguru import logger

from features.steps.src.exception_handler import exception_handler


class IocCommandQueue:
    def __init__(self):
        self._running = True
        self._soft_stop = False
        self.direct_queue = queue.Queue()
        self.ioc_exec_direct_queue = queue.Queue()
        self.ioc_register_direct_queue = queue.Queue()
        self._soft_stop_waiter_counter = 0

    def commands_worker(self, data):
        self.data = data
        while self._running:
            self.before_each_cycle()

            self.queue_without_ioc()
            if self.ioc_register_queue():
                continue
            self.ioc_execution_queue()

            if self.direct_queue.qsize() == 0:
                if self.ioc_exec_direct_queue.qsize() == 0:
                    if self.ioc_register_direct_queue.qsize() == 0:
                        if self._soft_stop:
                            self._soft_stop_waiter_counter -= 1
                if self._soft_stop_waiter_counter < 0:
                    break

    def queue_without_ioc(self):
        try:
            cmd = self.queue_handler(self.direct_queue,
                                     "direct_queue")
            if cmd is not None:
                try:
                    cmd.execute()
                    logger.info("direct_queue execute command:")
                    logger.info(cmd)
                except Exception as ex:
                    logger.exception("exception:")
                    logger.exception(ex)
                    exception_handler(self.direct_queue, cmd, ex)
        except Exception as ex:
            logger.exception("exception:")
            logger.exception(ex)
            pass

    def ioc_register_queue(self):
        try:
            ioc_reg_cmd = self.queue_handler(
                self.ioc_register_direct_queue,
                "ioc_register_direct_queue")
            if ioc_reg_cmd is not None:
                method_reg_name = ioc_reg_cmd[0]
                method_real_name = ioc_reg_cmd[1]
                self.data.ioc.resolve(key="IoC.register",
                                      registered_name=method_reg_name,
                                      called_method=method_real_name
                                      ).execute()
                logger.info(method_reg_name)
                logger.info(method_real_name)
                # для того чтобы сначала все команды зарегистрировались:
                return True
        except Exception as ex:
            logger.exception("exception:")
            logger.exception(ex)
            exception_handler(self.ioc_exec_direct_queue, ioc_reg_cmd, ex)
        return False

    def ioc_execution_queue(self):
        try:
            ioc_cmd = self.queue_handler(self.ioc_exec_direct_queue,
                                         "ioc_exec_direct_queue")
            if ioc_cmd is not None:
                self.data.ioc.resolve(ioc_cmd['command'],
                                      *ioc_cmd['argv'],
                                      **ioc_cmd['kwargs']).execute()
                logger.info("ioc_exec_direct_queue execute command:")
                logger.info(ioc_cmd['command'])
                logger.info(ioc_cmd['argv'])
                logger.info(ioc_cmd['kwargs'])
        except Exception as ex:
            logger.exception("exception:")
            logger.exception(ex)
            exception_handler(self.ioc_exec_direct_queue, ioc_cmd, ex)

    def queue_handler(self, current_queue, name="queue"):
        cmd = None
        try:
            cmd = current_queue.get_nowait()
            current_queue.task_done()
            logger.info(f"{name} get command:")
            logger.info(cmd)
        except queue.Empty:
            pass
        except Exception as ex:
            logger.exception("exception:")
            logger.exception(ex)
        return cmd

    def set_wait_command_appearance(self, value):
        self._soft_stop_waiter_counter = value

    def before_each_cycle(self):
        time.sleep(1)

    def add_command(self, cmd):
        self.direct_queue.put(cmd)

    def add_ioc_command(self, command_name: str, *argv, **kwargs):
        ioc_command = {}
        ioc_command['command'] = command_name
        ioc_command['argv'] = argv
        ioc_command['kwargs'] = kwargs
        self.ioc_exec_direct_queue.put(ioc_command)

    def register_ioc_command(self, name: str, method):
        self.ioc_register_direct_queue.put((name, method))

    def stop(self):
        self._running = False

    def soft_stop(self):
        self._soft_stop = True
